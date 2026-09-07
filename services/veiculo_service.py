from domain.entities import Veiculo
from domain.exceptions import DuplicateEntityError, InvalidIdentifierError
from repositories.interfaces import IRepositoryManager, IVeiculoRepository
from services.commands import UpdateVeiculoCommand


class VeiculoService:
    """Domain service for Vehicle use cases."""

    def __init__(self, db_manager: IRepositoryManager):
        self._db_manager = db_manager

    def _check_veiculos_dont_exist(
        self, veiculos: list[Veiculo], repo: IVeiculoRepository
    ) -> None:
        new_num_veics = [v.vehicle_number for v in veiculos]
        if new_num_veics:
            existing = repo.get_by_ids(new_num_veics)
            if existing:
                existing_veiculos = ", ".join(str(e.vehicle_number) for e in existing)
                raise DuplicateEntityError(
                    "veículos",
                    [e.vehicle_number for e in existing],
                    message=f"Os seguintes veículos já existem e não podem ser sobrescritos: {existing_veiculos}",
                )

    def get_veiculos(self) -> list[Veiculo]:
        """Retrieve vehicles from the database as domain entities."""
        with self._db_manager.session() as session:
            repo = session.get_veiculo_repository()
            return repo.get_all()

    def insert_veiculos(self, veiculos: list[Veiculo]) -> int:
        """Insert a list of vehicle domain entities into the database."""
        with self._db_manager.session() as session:
            repo = session.get_veiculo_repository()
            self._check_veiculos_dont_exist(veiculos, repo)
            if not veiculos:
                return 0
            return repo.insert_bulk(veiculos)

    def update_veiculos(self, commands: list[UpdateVeiculoCommand]) -> int:
        """Update a list of vehicles in the database from update commands."""
        num_veics = [cmd.vehicle_number for cmd in commands]
        if not num_veics:
            return 0

        with self._db_manager.session() as session:
            repo = session.get_veiculo_repository()
            existing = repo.get_by_ids(num_veics)
            existing_map = {v.vehicle_number: v for v in existing}

            updated_ids = set()
            to_update: list[Veiculo] = []
            for cmd in commands:
                if cmd.vehicle_number in existing_map:
                    veiculo = existing_map[cmd.vehicle_number]
                    if cmd.license_plate is not None:
                        veiculo.license_plate = cmd.license_plate
                    if cmd.active is not None:
                        if not cmd.active:
                            veiculo.deactivate(cmd.deregistration_date)
                        else:
                            veiculo.activate()
                    elif cmd.deregistration_date is not None:
                        veiculo.deregistration_date = cmd.deregistration_date

                    if cmd.vehicle_number not in updated_ids:
                        to_update.append(veiculo)
                        updated_ids.add(cmd.vehicle_number)

            if not to_update:
                return 0

            return repo.update_bulk(to_update)

    def delete_veiculos(self, num_veic: str | int) -> int:
        """Delete a vehicle from the database by its vehicle number."""
        try:
            num_veic_int = int(num_veic)
        except ValueError:
            raise InvalidIdentifierError(
                "Veículo", num_veic, message="Número do veículo inválido"
            )

        with self._db_manager.session() as session:
            repo = session.get_veiculo_repository()
            return repo.delete(num_veic_int)
