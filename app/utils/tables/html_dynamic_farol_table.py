import multiprocessing as mp
import pandas as pd
from typing import List


def process_row(
    index_values,
    row_data,
    df_combined_cache,
    score_farol_map,
    ordem_pilares,
    dataframe_columns,
):
    row_html = "<tr>"

    # Adiciona índice à linha
    for index_column in index_values:
        row_html += f"<td class='index'>{index_column}</td>"

    # Itera sobre os pilares
    for pilar in ordem_pilares:
        if pilar in dataframe_columns:
            # Itera sobre os temas de cada pilar
            for tema in dataframe_columns[pilar]:
                valor = row_data.get((pilar, tema), 0)
                icone_color = None
                icone_score = None
                df_agencia_pilar_tema = df_combined_cache.get((pilar, tema))

                if df_agencia_pilar_tema is not None:
                    agencia_data = df_agencia_pilar_tema.get(index_values[0])
                    if agencia_data:
                        icone_color = score_farol_map.get(
                            agencia_data["FAROL"], {}
                        ).get("color", "white")
                        icone_score = score_farol_map.get(
                            agencia_data["FAROL"], {}
                        ).get("icon", "bi bi-circle-fill")

                try:
                    valor = f"{valor:.2f}"
                except Exception:
                    valor = "-"
                    icone_color = None
                    icone_score = None

                # Adiciona a célula com o ícone e o valor
                row_html += f"""
                    <td data-column="{pilar}-{tema}" style="color: black; text-align: center; min-width: 50px;">
                        <div style="display: flex;">
                            <div style="width: 50%; display: flex; justify-content: flex-end;">
                                <span class="{icone_score}" style="color: {icone_color}; padding-right: 5px;"></span>
                            </div>
                            <div style="width: 50%; display: flex; justify-content: flex-start;">{valor}</div>
                        </div>
                    </td>
                """
    row_html += "</tr>"
    return row_html


def generate_html_table_parallel(
    dataframe: pd.DataFrame,
    df_combined: pd.DataFrame,
    score_farol_map: dict,
    index_columns: List[str],
    score_pilar_selected: List[str],
    rows_per_page: int = 10,
) -> str:
    # Reorganiza as colunas e prepara os dados
    dataframe = rearranja_coluna_score_pilar(dataframe)
    ordem_pilares = score_pilar_selected + ["GLOBAL"]
    dataframe_aux = dataframe.to_dict("index")

    # Cache de df_combined para otimizar a busca
    df_combined_cache = {
        (pilar, tema): df_combined[
            (df_combined["PILAR"] == pilar) & (df_combined["TEMA"] == tema)
        ]
        .set_index("AGENCIA")
        .to_dict("index")
        for pilar in ordem_pilares
        for tema in dataframe[pilar].columns
        if pilar in dataframe.columns.levels[0]
    }

    dataframe_columns = {
        pilar: dataframe[pilar].columns
        for pilar in ordem_pilares
        if pilar in dataframe.columns.levels[0]
    }

    # Geração paralela das linhas da tabela
    with mp.Pool(mp.cpu_count()) as pool:
        rows_html = pool.starmap(
            process_row,
            [
                (
                    index_values,
                    row_data,
                    df_combined_cache,
                    score_farol_map,
                    ordem_pilares,
                    dataframe_columns,
                )
                for index_values, row_data in dataframe_aux.items()
            ],
        )

    # Monta o HTML final
    html_string = """<div id="table-container"><table id="emp-table"><thead><tr>"""
    col_index = len(index_columns)

    for index_column in index_columns:
        html_string += f'<th class="index" rowspan="2">{index_column}</th>'

    for pilar in ordem_pilares:
        if pilar in dataframe.columns.levels[0]:
            qtd_temas_no_pilar = len(dataframe[pilar].columns)
            html_string += f'<th colspan="{qtd_temas_no_pilar}" style="border: 1px solid #D5D5DB; background-color: #EFF2F6">{pilar}</th>'

    html_string += "</tr><tr>"

    for pilar in ordem_pilares:
        if pilar in dataframe.columns.levels[0]:
            for tema in dataframe[pilar].columns:
                col_index += 1
                html_string += f"""<th class="sortable" data-column="{pilar}-{tema}" style="min-width: 100px; background-color: #F8F9FB;">{tema}</th>"""
    html_string += "</tr></thead><tbody id='table-body'>"

    # Adiciona as linhas geradas em paralelo
    html_string += "".join(rows_html)

    html_string += """</tbody></table><div class="pagination" id="pagination"></div></div></body></html>"""

    # Adiciona CSS e JS ao HTML final
    html_string += f"<style>{st.session_state['css_tabela_html_score_farol']}</style>"
    js_script = st.session_state["javascript_tabela_html_score_farol"].replace(
        "str(rows_per_page)", str(rows_per_page)
    )
    html_string += f"<script>{js_script}</script>"

    return html_string, dataframe
