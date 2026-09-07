from io import BytesIO
from unittest.mock import MagicMock, patch

import pytest

from infrastructure.parsers.exceptions import (
    DocumentParsingError,
    InvalidDocumentDataError,
)
from infrastructure.parsers.pyingestion.pyingestion_extractor import (
    PyIngestionDocumentExtractor,
)


def test_extractor_clone():
    mock_in = MagicMock()
    mock_trans = MagicMock()
    mock_out = MagicMock()

    extractor = PyIngestionDocumentExtractor(mock_in, mock_trans, mock_out)
    cloned = extractor.clone()

    assert cloned.input_stream_class == mock_in
    assert cloned.transform_stream_class == mock_trans
    assert cloned.write_stream_factory == mock_out
    assert cloned is not extractor


def test_extractor_lifecycle_callbacks():
    extractor = PyIngestionDocumentExtractor(MagicMock(), MagicMock(), MagicMock())
    session = MagicMock()

    # 1. _on_start
    extractor._on_start(session, total_files=3)

    # 2. _on_page_processed (success and failure)
    extractor._on_page_processed(
        session,
        success=True,
        extracted_pages=1,
        error_pages=0,
        page_index=1,
        total_pages=1,
    )
    extractor._on_page_processed(
        session,
        success=False,
        extracted_pages=0,
        error_pages=1,
        page_index=1,
        total_pages=1,
    )

    # 3. _on_error with exception kwarg
    err_exc = ValueError("Something failed")
    extractor._on_error(session, "Error description", exception=err_exc)
    assert extractor._last_error == err_exc

    # 4. _on_error without exception kwarg (fallback)
    extractor._on_error(session, "Fallback error description")
    assert isinstance(extractor._last_error, InvalidDocumentDataError)
    assert "Fallback error description" in str(extractor._last_error)

    # 5. _on_complete
    extractor._on_complete(session, successful_pages=5, total_pages=5)


def test_extractor_successful_pipeline():
    mock_in_instance = MagicMock()
    mock_in_class = MagicMock(return_value=mock_in_instance)

    mock_trans_instance = MagicMock()
    mock_trans_class = MagicMock(return_value=mock_trans_instance)

    mock_out_instance = MagicMock()
    mock_out_instance.processor.total_processed = 50
    mock_out_instance.processor.inserted_count = 45
    mock_out_instance.processor.ignored_count = 5
    mock_out_factory = MagicMock(return_value=mock_out_instance)

    extractor = PyIngestionDocumentExtractor(
        mock_in_class, mock_trans_class, mock_out_factory
    )

    with patch(
        "infrastructure.parsers.pyingestion.pyingestion_extractor.Gaia"
    ) as mock_gaia_cls:
        mock_gaia = mock_gaia_cls.return_value
        mock_gaia.process.return_value = True

        result = extractor.extract(BytesIO(b"fake data"))

        assert result["rows_processed"] == 50
        assert result["inserted"] == 45
        assert result["ignored"] == 5
        mock_out_instance.flush.assert_called_once()


def test_extractor_pipeline_failure_with_last_error():
    mock_in_class = MagicMock()
    mock_trans_class = MagicMock()
    mock_out_factory = MagicMock()

    extractor = PyIngestionDocumentExtractor(
        mock_in_class, mock_trans_class, mock_out_factory
    )
    custom_error = InvalidDocumentDataError("Invalid document structure")

    with patch(
        "infrastructure.parsers.pyingestion.pyingestion_extractor.Gaia"
    ) as mock_gaia_cls:
        mock_gaia = mock_gaia_cls.return_value

        def fail_process(*args, **kwargs):
            session = kwargs.get("session")
            if session:
                extractor._on_error(session, "Extraction error", exception=custom_error)
            return False

        mock_gaia.process.side_effect = fail_process

        with pytest.raises(InvalidDocumentDataError) as exc_info:
            extractor.extract(BytesIO(b"fake data"))
        assert "Invalid document structure" in str(exc_info.value)


def test_extractor_pipeline_failure_without_last_error():
    mock_in_class = MagicMock()
    mock_trans_class = MagicMock()
    mock_out_factory = MagicMock()

    extractor = PyIngestionDocumentExtractor(
        mock_in_class, mock_trans_class, mock_out_factory
    )

    with patch(
        "infrastructure.parsers.pyingestion.pyingestion_extractor.Gaia"
    ) as mock_gaia_cls:
        mock_gaia = mock_gaia_cls.return_value
        mock_gaia.process.return_value = False

        with pytest.raises(DocumentParsingError) as exc_info:
            extractor.extract(BytesIO(b"fake data"))
        assert "Extraction pipeline failed or was aborted." in str(exc_info.value)


def test_extractor_pipeline_unexpected_exception_wrapped():
    mock_in_class = MagicMock()
    mock_trans_class = MagicMock()
    mock_out_factory = MagicMock()

    extractor = PyIngestionDocumentExtractor(
        mock_in_class, mock_trans_class, mock_out_factory
    )

    with patch(
        "infrastructure.parsers.pyingestion.pyingestion_extractor.Gaia"
    ) as mock_gaia_cls:
        mock_gaia = mock_gaia_cls.return_value
        mock_gaia.process.side_effect = RuntimeError("Unexpected internal crash")

        with pytest.raises(DocumentParsingError) as exc_info:
            extractor.extract(BytesIO(b"fake data"))
        assert "PyIngestion pipeline failed: Unexpected internal crash" in str(
            exc_info.value
        )
