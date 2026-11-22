param(
    [Parameter(Mandatory = $true)][string]$Source,
    [Parameter(Mandatory = $true)][string]$Template,
    [Parameter(Mandatory = $true)][string]$Output
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

function Find-ContentBounds {
    param(
        [System.Drawing.Bitmap]$Bitmap,
        [int]$X0,
        [int]$X1,
        [int]$Y0,
        [int]$Y1
    )
    $minX = $X1
    $minY = $Y1
    $maxX = $X0
    $maxY = $Y0
    for ($y = $Y0; $y -lt $Y1; $y += 2) {
        for ($x = $X0; $x -lt $X1; $x += 2) {
            $c = $Bitmap.GetPixel($x, $y)
            if ([Math]::Max($c.R, [Math]::Max($c.G, $c.B)) -gt 18) {
                if ($x -lt $minX) { $minX = $x }
                if ($x -gt $maxX) { $maxX = $x }
                if ($y -lt $minY) { $minY = $y }
                if ($y -gt $maxY) { $maxY = $y }
            }
        }
    }
    if ($maxX -lt $minX -or $maxY -lt $minY) { throw 'No subject pixels found.' }
    return [System.Drawing.Rectangle]::FromLTRB(
        [Math]::Max($X0, $minX - 2),
        [Math]::Max($Y0, $minY - 2),
        [Math]::Min($X1, $maxX + 3),
        [Math]::Min($Y1, $maxY + 3)
    )
}

$src = [System.Drawing.Bitmap]::FromFile((Resolve-Path -LiteralPath $Source))
$tpl = [System.Drawing.Bitmap]::FromFile((Resolve-Path -LiteralPath $Template))
try {
    $subjectBottom = [int]($src.Height * 0.86)
    $third = [int]($src.Width / 3)
    $bounds = @(
        (Find-ContentBounds $src 0 $third 0 $subjectBottom),
        (Find-ContentBounds $src $third (2 * $third) 0 $subjectBottom),
        (Find-ContentBounds $src (2 * $third) $src.Width 0 $subjectBottom)
    )

    $targetLeft = 52
    $targetRight = 1995
    $targetTop = 206
    $targetBottom = 912
    $targetHeight = $targetBottom - $targetTop + 1
    $maxHeight = [int](($bounds | ForEach-Object { $_.Height } | Measure-Object -Maximum).Maximum)
    $scale = $targetHeight / [double]$maxHeight
    [int[]]$scaledWidths = @($bounds | ForEach-Object { [int][Math]::Round($_.Width * $scale) })
    [int[]]$scaledHeights = @($bounds | ForEach-Object { [int][Math]::Round($_.Height * $scale) })
    $sumWidths = [int](($scaledWidths | Measure-Object -Sum).Sum)
    $available = [int]($targetRight - $targetLeft + 1 - $sumWidths)
    $gap = [int][Math]::Floor($available / 2)
    if ($gap -lt 0) { throw 'Subjects cannot fit target frame at a common scale.' }

    [int[]]$xPositions = @(
        [int]$targetLeft,
        [int]($targetLeft + [int]$scaledWidths[0] + $gap),
        [int]($targetRight - [int]$scaledWidths[2] + 1)
    )

    $canvas = New-Object System.Drawing.Bitmap 2048, 1152, ([System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
    $g = [System.Drawing.Graphics]::FromImage($canvas)
    try {
        $g.Clear([System.Drawing.Color]::Black)
        $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
        $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
        for ($i = 0; $i -lt 3; $i++) {
            $dest = New-Object System.Drawing.Rectangle(
                $xPositions[$i],
                ($targetBottom - $scaledHeights[$i] + 1),
                $scaledWidths[$i],
                $scaledHeights[$i]
            )
            $g.DrawImage($src, $dest, $bounds[$i], [System.Drawing.GraphicsUnit]::Pixel)
        }

        $barStart = $tpl.Height - 1
        for ($y = 0; $y -lt $tpl.Height; $y++) {
            $c = $tpl.GetPixel([int]($tpl.Width / 2), $y)
            if ($c.G -gt 150 -and $c.R -gt 100 -and $c.B -lt 100) { $barStart = $y; break }
        }
        $barSrc = New-Object System.Drawing.Rectangle(0, $barStart, $tpl.Width, ($tpl.Height - $barStart))
        $barDest = New-Object System.Drawing.Rectangle(0, $barStart, 2048, ($tpl.Height - $barStart))
        $g.DrawImage($tpl, $barDest, $barSrc, [System.Drawing.GraphicsUnit]::Pixel)
    }
    finally {
        $g.Dispose()
    }

    $parent = Split-Path -Parent $Output
    if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
    $canvas.Save($Output, [System.Drawing.Imaging.ImageFormat]::Png)
    $canvas.Dispose()

    [PSCustomObject]@{
        Output = (Resolve-Path -LiteralPath $Output).Path
        Width = 2048
        Height = 1152
        Scale = [Math]::Round($scale, 4)
        Gap = $gap
        BarStart = $barStart
    }
}
finally {
    $src.Dispose()
    $tpl.Dispose()
}
