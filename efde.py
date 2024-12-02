import datetime
import numpy as np
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

now = int(datetime.datetime.now().timestamp())
start_ts = now - 3 * 30 * 24 * 60 * 60


@st.cache_data()
def make_data():
    df = pd.DataFrame(
        {
            "AGENCIA": [
                "Agencia 1",
                "Agencia 2",
                "Agencia 3",
                "Agencia 4",
                "Agencia 5",
            ],
            "UF": ["SP", "RJ", "MG", "BA", "PR"],
            "PERFORMANCE": [80, 90, 85, 88, 92],
            "PERFORMANCE_TCX": [80, 90, 85, 88, 92],
            "PERFORMANCE_ATM": [80, 90, 85, 88, 92],
            "RISCOS": [5, 3, 4, 2, 6],
            "RISCOS_FB": [5, 3, 4, 2, 6],
        }
    )
    return df


df = make_data()
gb = GridOptionsBuilder.from_dataframe(df)

# Configuração das colunas
gb.configure_default_column(editable=False)
grid_options = gb.build()

columns_mapping = {
    "PERFORMANCE": ["PERFORMANCE_TCX", "PERFORMANCE_ATM"],
    "RISCOS": ["RISCOS_FB"],
}

for col, cols in columns_mapping.items():
    list_cond = []
    list_html = []
    for c in cols:
        list_cond.append(f"const {c.lower()} = this.params.data.{c};")
        list_html.append(f"<li><strong>{c}:</strong> ${c.lower()}</li>")

    jsfnc = f"""
    class BtnCellRenderer {{
        init(params) {{
            this.params = params;
            this.eGui = document.createElement('div');
            
            const buttonText = this.params.value;

            this.eGui.innerHTML = `
            <span>
                <button id='click-button' 
                    class='btn-simple' 
                    style='color: ${{this.params.color}}; background-color: white; border: none;'>${{buttonText}}</button>
            </span>
            `;
            this.eButton = this.eGui.querySelector('#click-button');
            this.btnClickedHandler = this.btnClickedHandler.bind(this);
            this.eButton.addEventListener('click', this.btnClickedHandler);
        }}

        getGui() {{
            return this.eGui;
        }}

        refresh() {{
            return true;
        }}

        destroy() {{
            if (this.eButton) {{
                this.eGui.removeEventListener('click', this.btnClickedHandler);
            }}
        }}

        btnClickedHandler(event) {{
            let modalHTML = "";
            const field = this.params.colDef.field;
            const cd_ponto = this.params.data.AGENCIA;
            
            // Definir título do modal
            const modalTitle = 'Agência {{cd_ponto}}';
            const columns = {cols};

            // Gerar os itens do modal com as colunas apropriadas
            let listItems = columns.map(colName => {{
                const value = this.params.data[colName];
                return `<li><strong>${{colName}}:</strong> ${{value}}</li>`;
            }}).join('');

            modalHTML = `
                <div id="custom-modal" style="
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    background-color: white;
                    border: none;
                    border-radius: 10px;
                    box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
                    padding-left: 40px;
                    padding-right: 40px;
                    padding-top: 20px;
                    padding-bottom: 20px;
                    color: black;
                    z-index: 1000;
                    line-height: 1.5;">
                    <div style="display: flex; flex-direction: row; align-items: center;">
                        <strong>${{modalTitle}}<strong>
                        <button id="close-modal" style="
                            background-color: white;
                            color: black;
                            border: 1px solid grey;
                            border-radius: 60px;
                            padding: 5px 10px;
                            margin-left: 10px;
                        ">x</button>
                    </div>
                    <ul style="list-style-type: disc; padding-left: 5px; font-size: 12px;">
                        ${{listItems}}
                    </ul>
                </div>
                <div id="modal-overlay" style="
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background-color: rgba(0, 0, 0, 0.5);
                    z-index: 999;
                "></div>
            `;

            // Adicionar o modal ao DOM
            document.body.insertAdjacentHTML('beforeend', modalHTML);

            // Fechar o modal ao clicar no botão de fechar
            document.getElementById('close-modal').addEventListener('click', () => {{
                document.getElementById('custom-modal').remove();
                document.getElementById('modal-overlay').remove();
            }});

            // Fechar o modal ao clicar fora do modal
            document.getElementById('modal-overlay').addEventListener('click', () => {{
                document.getElementById('custom-modal').remove();
                document.getElementById('modal-overlay').remove();
            }});
        }}
    }};
    """

    BtnCellRenderer = JsCode(jsfnc)
    grid_options["columnDefs"].append(
        {
            "field": col,
            "headerName": col,
            "cellRenderer": BtnCellRenderer,
            "cellRendererParams": {"color": "red", "border": None},
        },
    )

# Exibir o DataFrame no AgGrid
AgGrid(
    df,
    theme="streamlit",
    key="table1",
    gridOptions=grid_options,
    allow_unsafe_jscode=True,
    fit_columns_on_grid_load=True,
    reload_data=False,
    try_to_convert_back_to_original_types=False,
)
