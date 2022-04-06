
dependencies = []
dev_dependencies = []

async def db_fill():
    errors = []
    try:
        for d in dependencies:
            try:
                await d()
            except Exception as exx:
                errors.append({
                    'error': exx,
                    'obj' : d.__name__                    
                })
        for d in dev_dependencies:
            await d()
        return str(errors)
    except Exception as ex:
        return str(ex)
