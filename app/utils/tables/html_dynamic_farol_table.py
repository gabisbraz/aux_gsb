from jinja2 import Template
import pandas as pd


def generate_html_table(
    dataframe: pd.DataFrame,
    df_combined: pd.DataFrame,
    score_farol_map: dict,
    index_columns: List[str],
    score_pilar_selected: List[str],
    rows_per_page: int = 10,
) -> str:
    # Template de HTML usando Jinja2 para uma renderização mais rápida
    template_str = """
    <div id="table-container">
        <table id="emp-table">
            <thead>
                <tr>
                    {% for index_column in index_columns %}
                        <th class="index" rowspan="2">{{ index_column }}</th>
                    {% endfor %}
                    {% for pilar in ordem_pilares %}
                        {% if pilar in dataframe.columns.levels[0] %}
                            <th colspan="{{ dataframe[pilar].columns | length }}" style="border: 1px solid #D5D5DB; background-color: #EFF2F6">{{ pilar }}</th>
                        {% endif %}
                    {% endfor %}
                </tr>
                <tr>
                    {% for pilar in ordem_pilares %}
                        {% if pilar in dataframe.columns.levels[0] %}
                            {% for tema in dataframe[pilar].columns %}
                                <th class="sortable" data-column="{{ pilar }}-{{ tema }}" style="min-width: 100px; background-color: #F8F9FB;">{{ tema }}</th>
                            {% endfor %}
                        {% endif %}
                    {% endfor %}
                </tr>
            </thead>
            <tbody id='table-body'>
                {% for index_values, row_data in dataframe_aux.items() %}
                    <tr>
                        {% for index_column in index_values %}
                            <td class='index'>{{ index_column }}</td>
                        {% endfor %}
                        {% for pilar in ordem_pilares %}
                            {% if pilar in dataframe.columns.levels[0] %}
                                {% for tema in dataframe[pilar].columns %}
                                    {% set valor = row_data.get((pilar, tema), 0) %}
                                    {% set df_agencia_pilar_tema = df_combined_cache.get((pilar, tema)) %}
                                    {% set icone_color = None %}
                                    {% set icone_score = None %}
                                    {% if df_agencia_pilar_tema is not none %}
                                        {% set icone_color = score_farol_map.get(df_agencia_pilar_tema[df_agencia_pilar_tema["AGENCIA"] == index_values[0]]["FAROL"].values[0], {}).get("color", "white") %}
                                        {% set icone_score = score_farol_map.get(df_agencia_pilar_tema[df_agencia_pilar_tema["AGENCIA"] == index_values[0]]["FAROL"].values[0], {}).get("icon", "bi bi-circle-fill") %}
                                    {% endif %}
                                    <td data-column="{{ pilar }}-{{ tema }}" style="color: black; text-align: center; min-width: 50px;">
                                        <div style="display: flex;">
                                            <div style="width: 50%; display: flex; justify-content: flex-end;">
                                                <span class="{{ icone_score }}" style="color: {{ icone_color }}; padding-right: 5px;"></span>
                                            </div>
                                            <div style="width: 50%; display: flex; justify-content: flex-start;">{{ valor }}</div>
                                        </div>
                                    </td>
                                {% endfor %}
                            {% endif %}
                        {% endfor %}
                    </tr>
                {% endfor %}
            </tbody>
        </table>
        <div class="pagination" id="pagination"></div>
    </div>
    <style>{{ css_file }}</style>
    <script>{{ js_file }}</script>
    """

    # Criação do template
    template = Template(template_str)

    # Cache de df_combined
    df_combined_cache = {
        (pilar, tema): df_combined[
            (df_combined["PILAR"] == pilar) & (df_combined["TEMA"] == tema)
        ]
        for pilar in score_pilar_selected + ["GLOBAL"]
        for tema in dataframe[pilar].columns
        if pilar in dataframe.columns.levels[0]
    }

    # Renderização do template
    html_string = template.render(
        index_columns=index_columns,
        dataframe=dataframe,
        ordem_pilares=score_pilar_selected + ["GLOBAL"],
        dataframe_aux=dataframe.to_dict("index"),
        df_combined_cache=df_combined_cache,
        score_farol_map=score_farol_map,
        css_file=st.session_state["css_tabela_html_score_farol"],
        js_file=st.session_state["javascript_tabela_html_score_farol"],
        rows_per_page=rows_per_page,
    )

    return html_string, dataframe
