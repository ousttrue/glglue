def get_desktop_scaling_factor():
    '''
    for high DPI desktop
    '''
    import platform
    if platform.platform().startswith('Windows'):
        from ctypes import windll
        desktop = windll.user32.GetDC(0)
        LogicalScreenHeight = windll.gdi32.GetDeviceCaps(
            desktop, 10)  # VERTRES
        PhysicalScreenHeight = windll.gdi32.GetDeviceCaps(
            desktop, 117)  # DESKTOPVERTRES
        return PhysicalScreenHeight / LogicalScreenHeight

    return 1
