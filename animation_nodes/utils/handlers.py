import bpy
from functools import wraps
from bpy.app.handlers import persistent

def validCallback(function):
    @wraps(function)
    def wrapper(self, context):
        function(self, context)
    return wrapper


# Event Handler System
###########################################################

alwaysHandlers = []
fileSavePreHandlers = []
fileLoadPostHandlers = []
versionUpdateHandlers = []
addonLoadPostHandlers = []
frameChangePostHandlers = []
depsgraphUpdatePostHandlers = []

renderPreHandlers = []
renderInitHandlers = []
renderCancelHandlers = []
renderCompleteHandlers = []

def eventHandler(event):
    def eventHandlerDecorator(function):
        if event == "ALWAYS": alwaysHandlers.append(function)
        if event == "FILE_SAVE_PRE": fileSavePreHandlers.append(function)
        if event == "FILE_LOAD_POST": fileLoadPostHandlers.append(function)
        if event == "VERSION_UPDATE": versionUpdateHandlers.append(function)
        if event == "ADDON_LOAD_POST": addonLoadPostHandlers.append(function)
        if event == "FRAME_CHANGE_POST": frameChangePostHandlers.append(function)
        if event == "DEPSGRAPH_UPDATE_POST": depsgraphUpdatePostHandlers.append(function)

        if event == "RENDER_INIT": renderInitHandlers.append(function)
        if event == "RENDER_PRE": renderPreHandlers.append(function)
        if event == "RENDER_CANCEL": renderCancelHandlers.append(function)
        if event == "RENDER_COMPLETE": renderCompleteHandlers.append(function)
        return function
    return eventHandlerDecorator

addonChanged = False
def always():
    for handler in alwaysHandlers:
        handler()

    global addonChanged
    if addonChanged:
        addonChanged = False
        for handler in addonLoadPostHandlers:
            handler()
    return 0

@persistent
def savePre(scene):
    for handler in fileSavePreHandlers:
        handler()

@persistent
def loadPost(scene):
    for handler in fileLoadPostHandlers:
        handler()

@persistent
def versionUpdate(self):
    for handler in versionUpdateHandlers:
        handler()

@persistent
def renderPre(scene):
    for handler in renderPreHandlers:
        handler()

@persistent
def frameChangedPost(scene, depsgraph):
    for handler in frameChangePostHandlers:
        handler(scene, depsgraph)

@persistent
def depsgraphUpdatePost(scene, depsgraph):
    for handler in depsgraphUpdatePostHandlers:
        handler(scene, depsgraph)

@persistent
def renderInitialized(scene):
    for handler in renderInitHandlers:
        handler()

@persistent
def renderCancelled(scene):
    for handler in renderCancelHandlers:
        handler()

@persistent
def renderCompleted(scene):
    for handler in renderCancelHandlers:
        handler()

def register():
    bpy.app.handlers.frame_change_post.append(frameChangedPost)
    bpy.app.handlers.depsgraph_update_post.append(depsgraphUpdatePost)
    bpy.app.timers.register(always, persistent = True)
    bpy.app.handlers.load_post.append(loadPost)
    bpy.app.handlers.version_update.append(versionUpdate)
    bpy.app.handlers.save_pre.append(savePre)

    bpy.app.handlers.render_complete.append(renderCompleted)
    bpy.app.handlers.render_init.append(renderInitialized)
    bpy.app.handlers.render_cancel.append(renderCancelled)
    bpy.app.handlers.render_pre.append(renderPre)


    global addonChanged
    addonChanged = True

def unregister():
    bpy.app.handlers.frame_change_post.remove(frameChangedPost)
    bpy.app.handlers.depsgraph_update_post.remove(depsgraphUpdatePost)
    bpy.app.handlers.load_post.remove(loadPost)
    bpy.app.handlers.version_update.remove(versionUpdate)
    bpy.app.handlers.save_pre.remove(savePre)
    bpy.app.timers.unregister(always)

    bpy.app.handlers.render_complete.remove(renderCompleted)
    bpy.app.handlers.render_init.remove(renderInitialized)
    bpy.app.handlers.render_cancel.remove(renderCancelled)
    bpy.app.handlers.render_pre.remove(renderPre)
