"""Dev APIs excluded from the OpenAPI Schema."""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, text

from app.db.session import get_session

router = APIRouter(prefix="/dev", tags=["dev"])


@router.get("/tables", include_in_schema=False)
def get_tables_with_row_counts(session: Session = Depends(get_session)) -> dict:
    """Get all public tables with row counts."""

    statement = text("""
        SELECT
            table_name,
            (
                xpath(
                    '/row/count/text()',
                    query_to_xml(
                        format(
                            'SELECT count(*) FROM public.%I',
                            table_name
                        ),
                        false,
                        true,
                        ''
                    )
                )
            )[1]::text::bigint AS row_count
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_type = 'BASE TABLE'
        ORDER BY table_name;
    """)

    result = session.exec(statement).all()

    tables = [
        {
            "table_name": row[0],
            "row_count": row[1],
        }
        for row in result
    ]

    return {"schema": "public", "tables": tables, "count": len(tables)}


@router.get("/{table_name}", include_in_schema=False)
def get_table_info(table_name: str, session: Session = Depends(get_session)):
    """Get information about a table."""

    statement = text("""
        SELECT
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = :table_name
        ORDER BY ordinal_position;
    """)

    result = session.exec(statement.params(table_name=table_name)).all()

    columns = [
        {
            "column_name": row[0],
            "data_type": row[1],
        }
        for row in result
    ]

    if not columns:
        raise HTTPException(
            status_code=404,
            detail=f"Table '{table_name}' not found",
        )

    return {"table_name": table_name, "columns": columns}


@router.get("/{table_name}/all", include_in_schema=False)
def get_all_table_rows(
    table_name: str, session: Session = Depends(get_session)
) -> dict:
    """Get all rows from a table."""

    statement = text(f'SELECT * FROM public."{table_name}";')

    result = session.exec(statement)

    rows = [dict(row._mapping) for row in result]

    return {"table_name": table_name, "rows": rows, "count": len(rows)}
