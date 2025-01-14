@router.post(
    '/', 
    response_model=CreateChatResponseSchema, 
    status_code=status.HTTP_201_CREATED,
    description='Endpoint creates a new chat, if a chat with this title exists, it returns 400 error',
    responses={
        status.HTTP_201_CREATED: {'model': CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def create_chat_handler(
    schema: CreateChatRequestSchema, 
    container: Container = Depends(init_container)
) -> CreateChatResponseSchema:
    '''Create new chat'''
    mediator: Mediator = container.resolve(Mediator) 

    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'error': exception.message},
        )
    return CreateChatResponseSchema.from_entity(chat)