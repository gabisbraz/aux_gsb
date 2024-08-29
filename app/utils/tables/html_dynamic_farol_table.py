from pathlib import Path

import pandas as pd

from typing import Dict, List
from dataclasses import dataclass
from streamlit.components.v1 import html


@dataclass
class Pilar:
    nome_front: str
    nome_etl: str
    cor: str


@dataclass
class ScorePilarMap:
    pilar_list: List[Pilar]


@dataclass
class Tema:
    nome_front: str
    nome_etl: str
    cor: str


@dataclass
class ScoreTemaMap:
    tema_list: List[Tema]


@dataclass
class Farol:
    nome_etl: str
    nome_front: str
    cor: str
    cor_fonte: str
    icones: str
    cor_icone: str
    valor_min: float
    valor_max: float


@dataclass
class ScoreFarolMap:
    farol_list: List[Farol]


def create_pivot_table_with_multindex(
    dataframe: pd.DataFrame,
    index: str = None,
    columns: List[str] = None,
    values: str = None,
    axis: int = 1,
) -> pd.DataFrame:
    df_pivot = dataframe.pivot_table(
        index=index, columns=columns, values=values, aggfunc="first"
    )

    return df_pivot.sort_index(axis=axis, level=list(range(len(columns))))


# Dados iniciais
data = {
    "ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Pilar": [
        "Pilar 1",
        "Pilar 1",
        "Pilar 3",
        "Pilar 4",
        "Pilar 1",
        "Pilar 2",
        "Pilar 3",
        "Pilar 4",
        "Pilar 1",
        "Pilar 2",
    ],
    "Tema": [
        "Tema 1",
        "Tema 1",
        "Tema 3",
        "Tema 1",
        "Tema 1",
        "Tema 3",
        "Tema 1",
        "Tema 2",
        "Tema 3",
        "Tema 1",
    ],
    "Valor": [8.5, 4.3, 6.2, 7.1, 5.4, 9.0, 6.5, 7.8, 5.6, 3.2],
}

df = pd.DataFrame(data)
repetitions = 4000 // len(df)
df = pd.concat([df] * repetitions, ignore_index=True)
df["ID"] = range(1, len(df) + 1)
df["UF"] = "SP"

df_pivot = create_pivot_table_with_multindex(
    dataframe=df, index=["ID", "UF"], columns=["Pilar", "Tema"], values="Valor"
)

score_pilar_map = ScorePilarMap(
    [
        Pilar("Pilar 1", "pilar1", "#FFCCCC"),
        Pilar("Pilar 2", "pilar2", "#CCFFCC"),
        Pilar("Pilar 3", "pilar3", "#CCCCFF"),
        Pilar("Pilar 4", "pilar4", "#FFFFCC"),
    ]
)

score_tema_map = ScoreTemaMap(
    [
        Tema("Tema 1", "tema1", "#FFAAAA"),
        Tema("Tema 2", "tema2", "#AAFFAA"),
        Tema("Tema 3", "tema3", "#AAAAFF"),
    ]
)

score_farol_map = ScoreFarolMap(
    [
        Farol("vermelho", "vermelho", "red", "black", "bi bi-x-circle", "red", 0, 3.33),
        Farol(
            "amarelo",
            "amarelo",
            "yellow",
            "black",
            "bi bi-exclamation-circle",
            "yellow",
            3.34,
            6.66,
        ),
        Farol(
            "verde",
            "verde",
            "green",
            "black",
            "bi bi-check-circle",
            "green",
            6.67,
            10,
        ),
    ]
)


def generate_html_table(
    dataframe: pd.DataFrame,
    score_farol_map: ScoreFarolMap,
    score_tema_map: ScoreTemaMap,
    score_pilar_map: ScorePilarMap,
    index_columns: List[str],
    rows_per_page: int = 7,
) -> str:
    def get_cell_format(value):
        for farol in score_farol_map.farol_list:
            if farol.valor_min <= round(float(value), 2) <= farol.valor_max:
                return farol.cor, farol.nome_front, farol.icones, farol.cor_icone
        return "white", "default", None, "black"

    css = """
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css">
    <style>
      table {
        width: 100%;
        border-collapse: collapse;
      }
      th, td {
        padding: 8px;
        text-align: center;
        border: 1px solid #D5D5DB;
        font-family: "sans serif";
      }
      td {
        background-color: white;
        font-family: "sans serif";
      }
      th {
        background-color: white;
        font-family: "sans serif";
      }
      th.agencia {
        position: sticky;
        left: 0;
        background-color: white;
        z-index: 3;
        color: black;
        font-family: "sans serif";
      }
      th.index {
        z-index: 3;
        position: sticky;
      }
      td.agencia {
        position: sticky;
        left: 0;
        background-color: white;
        z-index: 2;
        border-radius: 0px;
        color: black;
      }
      .filter-select {
        width: 100%;
      }
      th[colspan] {
        border-top-left-radius: 0px;
        border-top-right-radius: 0px;
        border-top: 0px;
        border-right: 0px;
        border-left: 0px;
      }
      th.sortable {
        cursor: pointer;
      }
      th.sortable.th-sort-asc::after {
        content: "\\25b4";
      }
      th.sortable.th-sort-desc::after {
        content: "\\25be";
      }
      th.sortable.th-sort-asc::after,
      th.sortable.th-sort-desc::after {
        margin-left: 5px;
      }
      th.sortable.th-sort-asc,
      th.sortable.th-sort-desc {
        background: rgba(0, 0, 0, 0.1);
      }
      .pagination {
        text-align: center;
        margin: 10px 0;
      }
      .pagination button {
        border: 1px solid #ddd;
        background-color: white;
        padding: 5px 10px;
        margin: 0 2px;
        cursor: pointer;
      }
      .pagination button.active {
        background-color: #007bff;
        color: white;
      }
      .pagination button.disabled {
        cursor: not-allowed;
        opacity: 0.5;
      }
    </style>"""

    html_string = """        
    <div id="table-container">
      <table id="emp-table">
        <thead>
          <tr>"""
    col_index = len(index_columns)

    def get_class_info(id_obj, id_value, arg_wanted, data_class_list):
        for obj in data_class_list:
            if getattr(obj, id_obj) == id_value:
                return getattr(obj, arg_wanted)
        return None

    for index_column in index_columns:
        html_string += f'<th class="index" rowspan="2">{index_column}</th>'

    for pilar in dataframe.columns.levels[0]:
        qtd_temas_no_pilar = len(dataframe[pilar].columns)
        pilar_info = (
            get_class_info("nome_etl", pilar, "cor", score_pilar_map.pilar_list)
            or "white"
        )
        html_string += f'<th colspan="{qtd_temas_no_pilar}" style="background-color: {pilar_info}; border: 1px solid #D5D5DB;">{pilar}</th>'
    html_string += "</tr><tr>"

    for pilar in dataframe.columns.levels[0]:
        for tema in dataframe[pilar].columns:
            col_index += 1
            tema_info = (
                get_class_info("nome_etl", tema, "cor", score_tema_map.tema_list)
                or "white"
            )
            html_string += f"""
      <th class="sortable" data-column="{pilar}-{tema}" style="background-color: {tema_info};">
        {tema}
      </th>"""
    html_string += "</tr></thead><tbody id='table-body'>"

    for _, row_data in dataframe.iterrows():
        html_string += "<tr>"
        for index_column in row_data.name:
            html_string += f"<td class='index'>{index_column}</td>"

        for pilar in dataframe.columns.levels[0]:
            for tema in dataframe[pilar].columns:
                valor = row_data.get((pilar, tema), 0)
                color_class, name_class, icone_score, cor_icone = get_cell_format(valor)
                html_string += f'<td class="{name_class}" data-column="{pilar}-{tema}" style="background-color: {color_class}; color: black;"><span class="{icone_score}" style="color: {cor_icone};"></span> {round(float(valor), 2):.2f}</td>'
        html_string += "</tr>"

    html_string += """
      </tbody>
    </table>
    <div class="pagination" id="pagination"></div>
    </div>
    </body>
    </html>
    """

    html_string += css

    js_script = (
        """
<script>
document.addEventListener('DOMContentLoaded', function() {
  const rowsPerPage = """
        + str(rows_per_page)
        + """;
  let currentPage = 1;
  let sortState = 0;  // 0: neutral, 1: ascending, 2: descending
  const maxVisiblePages = 5;

  // Function to render the table based on the current page
  function renderTable() {
    const rows = Array.from(document.querySelectorAll('#emp-table tbody tr'));
    const start = (currentPage - 1) * rowsPerPage;
    const end = start + rowsPerPage;

    // Hide all rows
    rows.forEach((row, index) => {
      row.style.display = (index >= start && index < end) ? '' : 'none';
    });

    // Update pagination
    updatePagination();
  }

  // Function to update pagination buttons
  function updatePagination() {
    const pagination = document.getElementById('pagination');
    const totalRows = document.querySelectorAll('#emp-table tbody tr').length;
    const totalPages = Math.ceil(totalRows / rowsPerPage);
    let startPage = Math.max(currentPage - Math.floor(maxVisiblePages / 2), 1);
    let endPage = Math.min(startPage + maxVisiblePages - 1, totalPages);

    pagination.innerHTML = '';

    if (totalPages > 1) {
      if (currentPage > 1) {
        const prevButton = document.createElement('button');
        prevButton.textContent = 'Previous';
        prevButton.addEventListener('click', () => {
          currentPage--;
          renderTable();
        });
        pagination.appendChild(prevButton);
      }

      if (startPage > 1) {
        const firstPageButton = document.createElement('button');
        firstPageButton.textContent = '1';
        firstPageButton.addEventListener('click', () => {
          currentPage = 1;
          renderTable();
        });
        pagination.appendChild(firstPageButton);

        const leftEllipsis = document.createElement('span');
        leftEllipsis.textContent = '...';
        pagination.appendChild(leftEllipsis);
      }

      for (let i = startPage; i <= endPage; i++) {
        const button = document.createElement('button');
        button.textContent = i;
        if (i === currentPage) {
          button.classList.add('active');
        }
        button.addEventListener('click', () => {
          currentPage = i;
          renderTable();
        });
        pagination.appendChild(button);
      }

      if (endPage < totalPages) {
        const rightEllipsis = document.createElement('span');
        rightEllipsis.textContent = '...';
        pagination.appendChild(rightEllipsis);

        const lastPageButton = document.createElement('button');
        lastPageButton.textContent = totalPages;
        lastPageButton.addEventListener('click', () => {
          currentPage = totalPages;
          renderTable();
        });
        pagination.appendChild(lastPageButton);
      }

      if (currentPage < totalPages) {
        const nextButton = document.createElement('button');
        nextButton.textContent = 'Next';
        nextButton.addEventListener('click', () => {
          currentPage++;
          renderTable();
        });
        pagination.appendChild(nextButton);
      }
    }
  }

  // Function to sort the table based on a column
  function sortTable(columnClass) {
    const rows = Array.from(document.querySelectorAll('#emp-table tbody tr'));
    const headerCells = Array.from(document.querySelectorAll('#emp-table thead th'));

    if (sortState === 0) {
      // Reset to the original order by ID
      rows.sort((a, b) => {
        const idA = parseInt(a.querySelector('td.index').innerText.trim());
        const idB = parseInt(b.querySelector('td.index').innerText.trim());
        return idA - idB;
      });
    } else if (sortState === 1) {
      // Sort rows ascending by the selected column
      rows.sort((a, b) => {
        const cellA = a.querySelector(`td[data-column="${columnClass}"]`).innerText.trim();
        const cellB = b.querySelector(`td[data-column="${columnClass}"]`).innerText.trim();
        const valueA = parseFloat(cellA) || 0;
        const valueB = parseFloat(cellB) || 0;
        return valueA - valueB;
      });
    } else if (sortState === 2) {
      // Sort rows descending by the selected column
      rows.sort((a, b) => {
        const cellA = a.querySelector(`td[data-column="${columnClass}"]`).innerText.trim();
        const cellB = b.querySelector(`td[data-column="${columnClass}"]`).innerText.trim();
        const valueA = parseFloat(cellA) || 0;
        const valueB = parseFloat(cellB) || 0;
        return valueB - valueA;
      });
    }

    // Re-render rows after sorting
    const tableBody = document.getElementById('table-body');
    tableBody.innerHTML = '';
    rows.forEach(row => {
      tableBody.appendChild(row);
    });

    // Cycle through sort states: neutral -> ascending -> descending -> neutral
    sortState = (sortState + 1) % 3;
    headerCells.forEach((th) => {
      th.classList.remove('th-sort-asc', 'th-sort-desc');
      if (th.dataset.column === columnClass) {
        if (sortState === 2) {
          th.classList.add('th-sort-asc');
        } else if (sortState === 0) {
          th.classList.add('th-sort-desc');
        }
      }
    });

    // Re-render the table with sorted data
    renderTable();
  }

  // Attach click event listeners to sortable headers
  document.querySelectorAll('th.sortable').forEach(th => {
    th.addEventListener('click', () => {
      sortTable(th.dataset.column);
    });
  });

  // Initialize the table and render it
  renderTable();
});
</script>
"""
    )

    html_string += js_script
    return html_string


html_output = generate_html_table(
    df_pivot,
    score_farol_map,
    score_tema_map,
    score_pilar_map,
    index_columns=["ID", "UF"],
)

html(html_output, height=500)
