import enum

class UserStatus(enum.Enum):
    NEW = "new"
    ACTIVE = "active"
    INACTIVE = "inactive"

class FoundItemStatus(enum.Enum):
    NEW = "new"
    ACTIVE = "active"
    INACTIVE = "inactive"

class RequestedItemStatus(enum.Enum):
    NEW = "new"
    ACTIVE = "active"
    INACTIVE = "inactive"