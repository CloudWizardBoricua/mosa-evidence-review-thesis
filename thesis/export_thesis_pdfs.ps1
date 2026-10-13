param(
    [Parameter(Mandatory=$true)][string]$OriginalSource,
    [Parameter(Mandatory=$true)][string]$OriginalCopy,
    [Parameter(Mandatory=$true)][string]$RevisedDocx,
    [Parameter(Mandatory=$true)][string]$OutputDirectory,
    [switch]$OnlyRevised,
    [switch]$OnlyOriginal
)
$ErrorActionPreference = 'Stop'
$sourcePath = (Resolve-Path -LiteralPath $OriginalSource).Path
$copyPath = (Resolve-Path -LiteralPath $OriginalCopy).Path
if ($sourcePath -eq $copyPath) { throw 'Export must use a separate formatted copy.' }
$sourceHash = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash
[void](New-Item -ItemType Directory -Force -Path $OutputDirectory)
$word = $null
$document = $null
function Normalize-Label([string]$value) {
    return [regex]::Replace($value.Trim([char[]]@(7, 13, 10, 32, 9)), '\s+', ' ')
}
function Update-OriginalNavigation($document) {
    $document.Repaginate()
    $locations = @{}
    $styles = @('Heading 1', 'Heading 2', 'Table Caption', 'Figure Caption', 'Equation Caption')
    foreach ($paragraph in $document.Paragraphs) {
        if ($styles -contains [string]$paragraph.Style.NameLocal) {
            $label = Normalize-Label $paragraph.Range.Text
            $location = $paragraph.Range.Duplicate
            $location.Collapse(1)
            $locations[$label] = [string]$location.Information(1)
            [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($location)
        }
    }
    $updated = 0
    $missing = [System.Collections.Generic.List[string]]::new()
    for ($tableNumber = 1; $tableNumber -le 4; $tableNumber++) {
        $table = $document.Tables.Item($tableNumber)
        for ($row = 1; $row -le $table.Rows.Count; $row++) {
            $label = Normalize-Label $table.Cell($row, 1).Range.Text
            if (-not $locations.ContainsKey($label)) { $missing.Add($label); continue }
            $cell = $table.Cell($row, 2)
            $range = $cell.Range.Duplicate
            # Word's cell range has one protected end marker in its offsets.
            # Exclude only that marker, otherwise the old last digit survives.
            $range.End = $range.End - 1
            $range.Text = $locations[$label]
            $cell.Range.Font.Size = 10.5
            $cell.Range.ParagraphFormat.FirstLineIndent = 0
            $cell.Range.ParagraphFormat.LeftIndent = 0
            $cell.Range.ParagraphFormat.RightIndent = 0
            $cell.Range.ParagraphFormat.Alignment = 2
            [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($range)
            $updated++
        }
    }
    if ($missing.Count) { throw ('Unresolved original navigation entries: ' + ($missing -join '; ')) }
    $document.Repaginate()
    return $updated
}
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $word.Options.UpdateLinksAtOpen = $false
    $word.Options.SaveNormalPrompt = $false
    $exports = @(
        @{Name='original'; Source=$copyPath},
        @{Name='revised'; Source=(Resolve-Path -LiteralPath $RevisedDocx).Path}
    )
    if ($OnlyRevised) { $exports = @($exports | Where-Object { $_.Name -eq 'revised' }) }
    if ($OnlyOriginal) { $exports = @($exports | Where-Object { $_.Name -eq 'original' }) }
    foreach ($export in $exports) {
        $document = $word.Documents.Open([string]$export.Source, $false, $false, $false)
        $document.Repaginate()
        [void]$document.Fields.Update()
        foreach ($toc in $document.TablesOfContents) { $toc.Update() }
        $document.Repaginate()
        if ($export.Name -eq 'original') {
            $entries = Update-OriginalNavigation $document
            Write-Output ('Original navigation: ' + $entries + ' verified page entries.')
        } else {
            foreach ($toc in $document.TablesOfContents) { $toc.UpdatePageNumbers() }
            [void]$document.Fields.Update()
            $document.Repaginate()
        }
        $document.Save()
        $pdfPath = Join-Path $OutputDirectory ('thesis-' + $export.Name + '.pdf')
        $pages = $document.ComputeStatistics(2)
        $document.ExportAsFixedFormat($pdfPath, 17, $false, 0, 0, 1, 1, 0, $true, $false, 1, $true, $true, $false)
        Write-Output ($export.Name + ': ' + $pages + ' pages; ' + $pdfPath)
        $document.Close(0)
        [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($document)
        $document = $null
    }
} finally {
    if ($null -ne $document) {
        $document.Close(0)
        [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($document)
    }
    if ($null -ne $word) {
        $word.Quit()
        [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($word)
    }
}
if ((Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash -ne $sourceHash) {
    throw 'The archived original Word source changed.'
}
Write-Output 'Archived original Word source hash is unchanged.'
