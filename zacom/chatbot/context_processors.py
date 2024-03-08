
def chat_history(request):
    """
    Context processor to retrieve the chat history from the session.
    """
    if 'chat_history' in request.session:
        return {'chat_history': request.session['chat_history']}
    else:
        return {'chat_history': {}}