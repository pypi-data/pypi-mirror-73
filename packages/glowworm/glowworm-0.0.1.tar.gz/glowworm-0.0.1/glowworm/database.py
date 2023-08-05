import abc
import typing

import glowworm.entity
import glowworm.exceptions

class Database(metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def get_all(self, keys:typing.Iterable[glowworm.entity.Key[glowworm.entity.T]]) -> typing.Dict[glowworm.entity.Key[glowworm.entity.T], glowworm.entity.T]:
		pass

	def get(self, key:glowworm.entity.Key[glowworm.entity.T]) -> typing.Optional[glowworm.entity.T]:
		return self.get_all([key]).get(key)

	def get_one(self, key:glowworm.entity.Key[glowworm.entity.T]) -> glowworm.entity.T:
		result = self.get(key)
		if result is None:
			raise glowworm.exceptions.EntityNotFoundError(f"Could not find entity with key {key}.")
		return result

	@abc.abstractmethod
	def put_all(self, entities:typing.Iterable[glowworm.entity.T]) -> None:
		pass

	def put(self, entity:glowworm.entity.T) -> None:
		return self.put_all([entity])
