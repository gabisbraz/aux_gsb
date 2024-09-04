import io
from pathlib import Path
from typing import List
import pandas as pd


def generate_html_table(
    dataframe: pd.DataFrame,
    df_combined: pd.DataFrame,
    score_farol_map: dict,
    index_columns: List[str],
    score_pilar_selected: List[str],
    rows_per_page: int = 10,
) -> str:
    """FUNÇÃO RESPONSÁVEL POR CRIAR O HTML DA TABELA DE SCORE FAROL."""

    # Lista para armazenar as partes do HTML
    html_parts = []

    # Carregamento do CSS
    if "css_tabela_html_score_farol" not in st.session_state:
        with open(
            file=str(
                Path(
                    DIR_ROOT_APP,
                    settings.get("PAGE_SCORE_GERAL.CSS_TABELA_HTML_SCORE_FAROL"),
                )
            ),
            mode="r",
            encoding="utf-8",
        ) as file:
            st.session_state["css_tabela_html_score_farol"] = file.read()
    css_file = st.session_state["css_tabela_html_score_farol"]

    # Adiciona o CSS da tabela HTML
    html_parts.append(
        f"""<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css"><style>{css_file}</style>"""
    )

    # Início da tabela
    html_parts.append('<div id="table-container"><table id="emp-table"><thead><tr>')

    # Reorganiza as colunas do dataframe principal
    dataframe = rearranja_coluna_score_pilar(dataframe)

    # Cabeçalhos de índice
    for index_column in index_columns:
        html_parts.append(f'<th class="index" rowspan="2">{index_column}</th>')

    # Pilar global sempre visível
    ordem_pilares = score_pilar_selected + ["GLOBAL"]

    # Cabeçalhos de Pilar
    for pilar in ordem_pilares:
        if pilar in dataframe.columns.levels[0]:
            qtd_temas_no_pilar = len(dataframe[pilar].columns)
            html_parts.append(
                f'<th colspan="{qtd_temas_no_pilar}" style="border: 1px solid #D5D5DB; background-color: #EFF2F6">{pilar}</th>'
            )

    # Linha de temas
    html_parts.append("</tr><tr>")
    for pilar in ordem_pilares:
        if pilar in dataframe.columns.levels[0]:
            for tema in dataframe[pilar].columns:
                html_parts.append(
                    f'<th class="sortable" data-column="{pilar}-{tema}" style="min-width: 100px; background-color: #F8F9FB;">{tema}</th>'
                )
    html_parts.append("</tr></thead><tbody id='table-body'>")

    # Linhas da tabela
    dataframe_aux = dataframe.to_dict("index")
    for index_values, row_data in dataframe_aux.items():
        html_parts.append("<tr>")
        for index_column in index_values:
            html_parts.append(f"<td class='index'>{index_column}</td>")

        df_agencia = df_combined.loc[df_combined["AGENCIA"] == index_values[0]]

        for pilar in ordem_pilares:
            if pilar in dataframe.columns.levels[0]:
                for tema in dataframe[pilar].columns:
                    valor = row_data.get((pilar, tema), 0)
                    icone_color = None
                    icone_score = None
                    df_agencia_pilar_tema = df_agencia.loc[
                        (df_agencia["PILAR"] == pilar) & (df_agencia["TEMA"] == tema)
                    ]
                    if not df_agencia_pilar_tema.empty:
                        icone_color = score_farol_map.get(
                            df_agencia_pilar_tema["FAROL"].values[0], {}
                        ).get("color", "white")
                        icone_score = score_farol_map.get(
                            df_agencia_pilar_tema["FAROL"].values[0], {}
                        ).get("icon", "bi bi-circle-fill")
                    try:
                        valor = f"{valor:.2f}"
                    except Exception:
                        valor = "-"
                        icone_color = None
                        icone_score = None

                    html_parts.append(
                        f'<td data-column="{pilar}-{tema}" style="color: black; text-align: center; min-width: 50px;">'
                        f'<div style="display: flex;">'
                        f'<div style="width: 50%; display: flex; justify-content: flex-end;">'
                        f'<span class="{icone_score}" style="color: {icone_color}; padding-right: 5px;"></span>'
                        f"</div>"
                        f'<div style="width: 50%; display: flex; justify-content: flex-start;">{valor}</div>'
                        f"</div></td>"
                    )
        html_parts.append("</tr>")

    # Fecha a tabela e adiciona paginação
    html_parts.append(
        "</tbody></table><div class='pagination' id='pagination'></div></div>"
    )

    # Adiciona o CSS ao final do HTML
    html_parts.append(f"<style>{css_file}</style>")

    # Carregamento do JavaScript
    if "javascript_tabela_html_score_farol" not in st.session_state:
        with open(
            file=str(
                Path(
                    DIR_ROOT_APP,
                    settings.get("PAGE_SCORE_GERAL.JAVASCRIPT_TABELA_HTML_SCORE_FAROL"),
                )
            ),
            mode="r",
            encoding="utf-8",
        ) as file:
            st.session_state["javascript_tabela_html_score_farol"] = file.read()
    js_file = st.session_state["javascript_tabela_html_score_farol"]
    js_file = js_file.replace("str(rows_per_page)", str(rows_per_page))

    # Adiciona o script JS ao HTML
    html_parts.append(f"<script>{js_file}</script>")

    # Retorna o HTML final concatenando as partes
    return "".join(html_parts), dataframe
