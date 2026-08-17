def calculate_graham_intrinsic_value(
    eps: float | None,
    growth_rate: float | None,
    aaa_yield: float
) -> float | None:
    """
    Calculates intrinsic value using Benjamin Graham's revised formula:
    V = (EPS * (8.5 + 2g) * 4.4) / Y
    
    Args:
        eps (float): Trailing or Forward Earnings Per Share.
        growth_rate (float): Expected annual growth rate in decimal (e.g., 0.10 for 10%).
        aaa_yield (float): Current AAA corporate bond yield percentage.
        
    Returns:
        float or None: Calculated intrinsic value per share.
    """
    if eps is None or eps <= 0 or aaa_yield <= 0:
        return None
        
    g_percent = (growth_rate or 0.05) * 100
    intrinsic_val = (eps * (8.5 + 2 * g_percent) * 4.4) / aaa_yield
    return round(intrinsic_val, 2)


def calculate_margin_of_safety(current_price: float | None, intrinsic_value: float | None) -> float | None:
    """
    Calculates Margin of Safety percentage.
    
    Returns:
        float or None: Margin of safety percentage.
    """
    if not current_price or not intrinsic_value or intrinsic_value <= 0:
        return None
        
    margin = ((intrinsic_value - current_price) / intrinsic_value) * 100
    return round(margin, 2)
