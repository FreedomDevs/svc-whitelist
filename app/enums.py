from svcLibs.codes import BaseOkCode, BaseErrorCode

class WhitelistCreatedOk(BaseOkCode):
    HTTPCODE = 201
    CODE = "WHITELIST_CREATED_OK"
    MESSAGE = "Пользователь успешно добавлен в whitelist"

class WhitelistRemovedOk(BaseOkCode):
    HTTPCODE = 200
    CODE = "WHITELIST_REMOVED_OK"
    MESSAGE = "Пользователь успешно удалён из whitelist"

class WhitelistCheckOk(BaseOkCode):
    HTTPCODE = 200
    CODE = "WHITELIST_CHECK_OK"
    MESSAGE = "Успешно получена информация по наличию игрока в whitelist"

class WhitelistAlreadyExists(BaseErrorCode):
    HTTPCODE = 400
    CODE = "WHITELIST_ALREADY_EXISTS"
    MESSAGE = "Пользователь уже в whitelist"

class WhitelistNotFound(BaseErrorCode):
    HTTPCODE = 404
    CODE = "WHITELIST_NOT_FOUND"
    MESSAGE = "Пользователь не в whitelist"
