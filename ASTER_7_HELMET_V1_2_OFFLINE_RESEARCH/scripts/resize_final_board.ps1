param(
    [Parameter(Mandatory = $true)][string]$Source,
    [Parameter(Mandatory = $true)][string]$Template,
    [Parameter(Mandatory = $true)][string]$Output
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$src = [System.Drawing.Bitmap]::FromFile((Resolve-Path -LiteralPath $Source))
$tpl = [System.Drawing.Bitmap]::FromFile((Resolve-Path -LiteralPath $Template))
try {
    $canvas = New-Object System.Drawing.Bitmap 2048, 1152, ([System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
    $g = [System.Drawing.Graphics]::FromImage($canvas)
    try {
        $g.Clear([System.Drawing.Color]::Black)
        $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
        $g.DrawImage($src, (New-Object System.Drawing.Rectangle(0, 0, 2048, 1152)))

        $barStart = $tpl.Height - 1
        for ($y = 0; $y -lt $tpl.Height; $y++) {
            $c = $tpl.GetPixel([int]($tpl.Width / 2), $y)
            if ($c.G -gt 150 -and $c.R -gt 100 -and $c.B -lt 100) { $barStart = $y; break }
        }
        $bar = New-Object System.Drawing.Rectangle(0, $barStart, 2048, ($tpl.Height - $barStart))
        $g.DrawImage($tpl, $bar, $bar, [System.Drawing.GraphicsUnit]::Pixel)
    }
    finally { $g.Dispose() }

    $parent = Split-Path -Parent $Output
    if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
    $canvas.Save($Output, [System.Drawing.Imaging.ImageFormat]::Png)
    $canvas.Dispose()
    [PSCustomObject]@{ Output = (Resolve-Path -LiteralPath $Output).Path; Width = 2048; Height = 1152; BarStart = $barStart }
}
finally {
    $src.Dispose()
    $tpl.Dispose()
}
