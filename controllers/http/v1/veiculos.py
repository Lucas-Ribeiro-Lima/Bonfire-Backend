from datetime import datetime

from flask import Blueprint

from controllers.http.spec import spec
from controllers.http.v1.dependencies import get_veiculo_service
from controllers.http.v1.schemas.common import MutationResponseDTO, create_api_response
from controllers.http.v1.schemas.veiculos import (
    VeiculoListRequestDTO,
    VeiculoListResponseDTO,
    VeiculoListUpdateRequestDTO,
)
from domain.entities import Veiculo
from services.commands import UpdateVeiculoCommand

veiculoBlueprint = Blueprint("veiculo", __name__)
_get_service = get_veiculo_service


@veiculoBlueprint.route("/veiculos", methods=["GET"])
@spec.validate(
    resp=create_api_response(VeiculoListResponseDTO, success_code=200),
    security={"BearerAuth": []},
    tags=["Veículos"],
)
def executeRouteGetVeiculo():
    """Get all vehicles."""
    service = _get_service()
    result = service.get_veiculos()
    return VeiculoListResponseDTO(veiculos=result), 200


@veiculoBlueprint.route("/veiculos", methods=["POST"])
@spec.validate(
    json=VeiculoListRequestDTO,
    resp=create_api_response(MutationResponseDTO, success_code=201),
    security={"BearerAuth": []},
    tags=["Veículos"],
)
def executeRoutePostVeiculos(json: VeiculoListRequestDTO):
    """Insert vehicles."""
    veiculos = [
        Veiculo(
            NUM_VEIC=int(item.NUM_VEIC),
            IDN_PLAC_VEIC=item.IDN_PLAC_VEIC,
            VEIC_ATIV_EMPR=bool(item.VEIC_ATIV_EMPR)
            if item.VEIC_ATIV_EMPR is not None
            else True,
            DAT_BAIX=datetime.fromisoformat(item.DAT_BAIX) if item.DAT_BAIX else None,
        )
        for item in json.root
    ]
    service = _get_service()
    response = service.insert_veiculos(veiculos)
    return (
        MutationResponseDTO(message="Veículos inseridos com sucesso", counter=response),
        201,
    )


@veiculoBlueprint.route("/veiculos", methods=["PATCH"])
@spec.validate(
    json=VeiculoListUpdateRequestDTO,
    resp=create_api_response(MutationResponseDTO, success_code=202),
    security={"BearerAuth": []},
    tags=["Veículos"],
)
def executeRoutePatchVeiculos(json: VeiculoListUpdateRequestDTO):
    """Update vehicles."""
    commands = [
        UpdateVeiculoCommand(
            vehicle_number=int(item.NUM_VEIC),
            license_plate=item.IDN_PLAC_VEIC,
            active=bool(item.VEIC_ATIV_EMPR)
            if item.VEIC_ATIV_EMPR is not None
            else None,
            deregistration_date=datetime.fromisoformat(item.DAT_BAIX)
            if item.DAT_BAIX
            else None,
        )
        for item in json.root
    ]
    service = _get_service()
    response = service.update_veiculos(commands)
    return (
        MutationResponseDTO(
            message="Veículos atualizados com sucesso", counter=response
        ),
        202,
    )


@veiculoBlueprint.route("/veiculos/<string:NUM_VEIC>", methods=["DELETE"])
@spec.validate(
    resp=create_api_response(MutationResponseDTO, success_code=202),
    security={"BearerAuth": []},
    tags=["Veículos"],
)
def executeRouteDeleteVeiculos(NUM_VEIC: str):
    """Delete a vehicle by its vehicle number."""
    service = _get_service()
    response = service.delete_veiculos(NUM_VEIC)
    return (
        MutationResponseDTO(message="Veículos deletados com sucesso", counter=response),
        202,
    )
