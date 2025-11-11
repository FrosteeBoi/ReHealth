def return_to_dashboard(frame, root, user):
    """
    Destroys current frame and returns user to the dashboard.
    """
    from dashboard import Dashboard
    frame.destroy()
    Dashboard(root, user)
