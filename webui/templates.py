class Messages:
    TITLE = "maps4FS"
    MAIN_PAGE_DESCRIPTION = (
        "Generate map templates for Farming Simulator from real places.  \n\n"
        "If some objects (buidings, fields, etc.) are missing or misplaced,  \nyou can edit them "
        "by yourself on the 🌎 [OpenStreetMap](https://www.openstreetmap.org/) website. \n\n"
        "💬 Join our [Discord server](https://discord.gg/Sj5QKKyE42) to get help, share your "
        "maps, or just chat.  \n"
        "🤗 If you like the project, consider supporting it on [Buy Me a Coffee](https://www.buymeacoffee.com/iwatkot).  \n"
        "📹 A complete step-by-step video tutorial is on [YouTube](https://www.youtube.com/watch?v=Nl_aqXJ5nAk&)!"
    )
    MAIN_PAGE_COMMUNITY_WARNING = (
        "🚜 Hey, farmer!  \n"
        "Do you know what **Docker** is? If yes, please consider running the application "
        "locally.  \n"
        "StreamLit community hosting has some limitations, such as:  \n"
        "🔸 Maximum map size is 2048x2048 meters.  \n"
        "🔸 Background terrain will not be generated.  \n"
        "🔸 Advanced settings are disabled.  \n"
        "🔸 Texture dissolving is disabled (they will look worse).  \n  \n"
        "If you run the application locally, you won't have any of these limitations "
        "and will be able to generate maps of any size with any settings you want and nice looking textures.  \n"
        "Learn more about the Docker version in the repo's "
        "[README](https://github.com/iwatkot/maps4fs?tab=readme-ov-file#option-2-docker-version).  \n"
        "Also, if you are familiar with Python, you can use the "
        "[maps4fs](https://pypi.org/project/maps4fs/) package to generate maps locally."
    )
    # TERRAIN_RELOAD = (
    #     "ℹ️ When opening the map first time in the Giants Editor, select the **terrain** object, "
    #     "open the **Terrain** tab in the **Attributes** window, scroll down to the end "
    #     "and press the **Reload material** button.  \n"
    #     "Otherwise you may (and will) face some glitches."
    # )
    # HEIGHT_SCALE_INFO = (
    #     "ℹ️ Remember to adjust the ***heightScale*** parameter in the Giants Editor to a value "
    #     "that suits your map. Learn more about it in repo's "
    #     "[README](https://github.com/iwatkot/maps4fs?tab=readme-ov-file#For-advanced-users)."
    # )
    COMMUNITY_ADVANCED_SETTINGS = (
        "💡 Advanced settings are disabled on StreamLit community hosting.  \n"
        "If you want to have more control over the terrain generation, consider running the "
        "application locally."
    )

    AUTO_PRESET_INFO = (
        "Auto preset will automatically apply different algorithms to make terrain more "
        "realistic. It's recommended for most cases. If you want to have more control over the "
        "terrain generation, you can disable this option and change the advanced settings."
    )
    AUTO_PRESET_DISABLED = (
        "Auto preset is disabled. In this case you probably receive a full black DEM "
        "image file. But it is NOT EMPTY. Dem image value range is from 0 to 65535, "
        "while on Earth the highest point is 8848 meters. So, unless you are not "
        "working with map for Everest, you probably can't see anything on the DEM image "
        "by eye, because it is too dark. You can use the "
        "multiplier option from Advanced settings to make the terrain more pronounced."
    )
    DEM_MULTIPLIER_INFO = (
        "This multiplier can be used to make the terrain more pronounced. "
        "By default the DEM file will be exact copy of the real terrain. "
        "If you want to make it more steep, you can increase this value. "
    )
    DEM_BLUR_RADIUS_INFO = (
        "This value is used to blur the elevation map. Without blurring the terrain "
        "may look too sharp and unrealistic. By default the blur radius is set to 21 "
        "which corresponds to a 21x21 pixel kernel. You can increase this value to make "
        "the terrain more smooth. Or make it smaller to make the terrain more sharp."
    )
    DEM_PLATEAU_INFO = (
        "This value is used to make the whole map higher or lower. "
        "This value will be added to each pixel of the DEM image, making it higher."
        "It can be useful if you're working on a plain area and need to add some "
        "negative height (to make rivers, for example)."
    )
    TOOLBOX_INFO = (
        "This section contains different tools that can be helpful for modders, grouped by "
        "the component of the map they are related to.  \n"
    )
    KNOWLEDGE_INFO = (
        "Here you can find some useful information about the different aspects of map modding."
    )
    FAQ_INFO = "Here you can find answers to the most frequently asked questions."
    ONLY_FULL_TILES_INFO = (
        "If checked only full tiles will be generated. If unchecked, the background terrain will "
        "be also generated as splitted tiles, e.g. N, NE, E, SE, S, SW, W, NW.  \n"
        "In most cases you don't need splitted tiles, so it's recommended to keep this option "
        "checked."
    )
    FIELD_PADDING_INFO = (
        "This value is used to add some padding around the fields. "
        "It will make the fields smaller, can be useful if they are too close to each other."
    )
    FARMLAND_MARGIN_INFO = (
        "This value is used to add some margin around the farmland. "
        "It can be useful because without the margin, the farmland will end exact on the same "
        "position as the field ends. This can cause some issues with gameplay."
    )
