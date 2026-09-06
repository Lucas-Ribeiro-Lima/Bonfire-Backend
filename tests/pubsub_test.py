import pytest

from infrastructure.parsers.exceptions import InvalidDocumentDataError
from infrastructure.parsers.pyingestion.pubsub import SyncBatchProcessor


def test_pubsub_unconsumed_columns_error():
    # Mock a processor function that raises the specific SQLAlchemy error
    def mock_processor(batch):
        raise ValueError("Unconsumed column names: placa, linha, data_vencimento")

    processor = SyncBatchProcessor(processor_func=mock_processor, batch_size=2)

    # We expect InvalidDocumentDataError to be raised when the flush occurs
    with pytest.raises(InvalidDocumentDataError) as excinfo:
        processor.publish({"col1": "val1"})
        processor.publish({"col2": "val2"})  # This triggers flush since batch_size=2

    assert (
        "O arquivo enviado possui formato estrutural inválido"
        in str(excinfo.value)
    )
    assert "placa, linha, data_vencimento" in str(excinfo.value)


def test_pubsub_generic_error():
    # Mock a processor function that raises a generic error
    def mock_processor(batch):
        raise ValueError("Database connection failed")

    processor = SyncBatchProcessor(processor_func=mock_processor, batch_size=1)

    # We expect the original ValueError to be raised
    with pytest.raises(ValueError) as excinfo:
        processor.publish({"col1": "val1"})

    assert "Database connection failed" in str(excinfo.value)
