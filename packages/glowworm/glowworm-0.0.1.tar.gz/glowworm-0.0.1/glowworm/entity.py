import typing

T = typing.TypeVar("T", bound="Entity")

class Key(typing.Generic[T]):
	def __init__(self, kind:typing.Type[T], key:typing.Union[str, int]) -> None:
		self.kind = kind
		self.key = key

	def __repr__(self) -> str:
		return f"{self.__class__.__name__}<{self.kind.__name__}, {self.key}>"

class Entity():
	key:Key["Entity"] # TODO: How the fuck do you type this?

	def __init__(self, **kwargs:typing.Any) -> None:
		for argument, value in kwargs.items():
			if argument not in self.__class__._get_fields():
				raise AttributeError(f"Attribute \"{argument}\" not allowed for entity type \"{self.__class__.__name__}\".")
			setattr(self, argument, value)

	@classmethod
	def _get_fields(cls) -> typing.Collection[str]:
		fields = set(cls.__annotations__.keys())
		for base in cls.__bases__:
			if issubclass(base, Entity):
				fields.update(base._get_fields())
		return fields

	@classmethod
	def _key(cls:typing.Type[T], key:typing.Union[str, int]) -> Key[T]:
		return Key(cls, key)

	def _to_dictionary(self) -> typing.Dict[str, typing.Any]:
		dictionary = {}
		for field in self.__class__._get_fields():
			dictionary[field] = getattr(self, field)
		return dictionary
