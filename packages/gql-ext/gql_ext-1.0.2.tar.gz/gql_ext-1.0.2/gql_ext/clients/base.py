def mount_to_app(app, cls, service_name, spec, params):
    async def mount(_):
        api = await cls.create(spec, **params)
        setattr(app, service_name, api)

        async def stop(__):
            await api.stop()

        app.on_shutdown.append(stop)

    app.on_startup.append(mount)
