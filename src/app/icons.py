import pygame


def build_icon(icon_type):
    """Return a 24x24 SRCALPHA surface for the given icon_type string."""
    if icon_type == "clue":
        return _clue_icon()
    if icon_type == "note":
        return _result_icon()
    return None


def _clue_icon():
    """Magnifying glass — used for new-clue side notes."""
    S = 3
    SIZE = 24 * S
    big = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA, 32)
    col  = (235, 235, 235, 255)
    fill = (235, 235, 235, 55)
    hi   = (255, 255, 255, 90)

    cx, cy, r = 28, 26, 17
    # Soft fill inside lens
    pygame.draw.circle(big, fill, (cx, cy), r - 2)
    # Lens ring
    pygame.draw.circle(big, col, (cx, cy), r, 4)
    # Inner highlight arc (top-left crescent)
    pygame.draw.circle(big, hi, (cx - 4, cy - 4), r - 7, 3)
    # Handle — rounded ends via circles + line
    hx1, hy1 = cx + r - 2, cy + r - 2
    hx2, hy2 = SIZE - 8, SIZE - 7
    hw = 7
    pygame.draw.line(big, col, (hx1, hy1), (hx2, hy2), hw)
    pygame.draw.circle(big, col, (hx1, hy1), hw // 2)
    pygame.draw.circle(big, col, (hx2, hy2), hw // 2)

    return pygame.transform.smoothscale(big, (24, 24))


def _result_icon():
    """Speech bubble with checkmark — used for interrogation result side notes."""
    S = 3
    SIZE = 24 * S
    big = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA, 32)
    col  = (235, 235, 235, 255)
    fill = (235, 235, 235, 40)

    # Rounded speech bubble body
    bx, by, bw, bh = 4, 3, SIZE - 8, SIZE - 18
    pygame.draw.rect(big, fill, (bx, by, bw, bh), border_radius=10)
    pygame.draw.rect(big, col,  (bx, by, bw, bh), 4, border_radius=10)
    # Tail pointing down-left
    tail = [(bx + 10, by + bh - 1), (bx + 6, by + bh + 14), (bx + 22, by + bh - 1)]
    pygame.draw.polygon(big, fill, tail)
    pygame.draw.polygon(big, col,  tail, 4)
    # Cover the bottom edge of the bubble over the tail join
    pygame.draw.line(big, col, (bx + 14, by + bh - 1), (bx + bw - 4, by + bh - 1), 5)
    # Bold checkmark inside bubble
    cx = SIZE // 2
    cy = by + bh // 2 - 4
    pts = [(cx - 16, cy + 2), (cx - 4, cy + 13), (cx + 16, cy - 12)]
    pygame.draw.lines(big, col, False, pts, 6)
    for pt in pts:
        pygame.draw.circle(big, col, pt, 3)

    return pygame.transform.smoothscale(big, (24, 24))
