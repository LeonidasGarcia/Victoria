from typing import Optional, List

import pandas
from pandas import DataFrame
from pandas.errors import EmptyDataError

from src.data.preset import Preset


class PresetsCentral:
    def __init__(self, root_file: str, trace_file: str):
        self.root_file = root_file
        self.trace_file = trace_file

        self.presets, self.presets_reference_trace = self.load_presets()

        if self.presets.empty:
            self.initial_load()

    def load_presets(self) -> tuple[DataFrame, DataFrame]:

        # -------------------------------------------------------------
        # 1. Definición de Tipos con Enteros Nulleables (SIN 'id')
        # -------------------------------------------------------------
        PRESETS_DTYPES = {
            "name": "string",
            "ram": "Int64",
            "program_size": "Int64",
            "page_size": "Int64",
            "program_count": "Int64",
        }
        TRACE_DTYPES = {
            "preset_id": "Int64",
            "pid": "Int64",
            "page": "Int64",
            "mode": "string",
        }

        try:
            # Cargar: index_col="id" maneja el ID. Usamos dtype solo para las columnas de datos.
            presets = pandas.read_csv(self.root_file, index_col="id", dtype=PRESETS_DTYPES)
            presets_reference_trace = pandas.read_csv(self.trace_file, index_col="id", dtype=TRACE_DTYPES)

            presets.index.name = "id"
            presets_reference_trace.index.name = "id"

            return presets, presets_reference_trace

        except FileNotFoundError:
            # Si el archivo no existe, lanza el error
            raise FileNotFoundError

        except pandas.errors.EmptyDataError:
            # -------------------------------------------------------------
            # 2. Crear DataFrames vacíos: Se definen solo las columnas de datos.
            # -------------------------------------------------------------

            # Crear el DataFrame con las columnas de datos y forzar los tipos
            presets = DataFrame(columns=PRESETS_DTYPES.keys()).astype(PRESETS_DTYPES)

            presets_reference_trace = DataFrame(columns=TRACE_DTYPES.keys()).astype(TRACE_DTYPES)

            # Establecer el nombre del índice
            presets.index.name = "id"
            presets_reference_trace.index.name = "id"

            return presets, presets_reference_trace

    def initial_load(self):
        temporal = Preset(
            id=-1,
            name="Localidad Temporal",
            ram=192,
            program_size=128,
            page_size=64,
            program_count=3,
            reference_trace=[
                (-1, 0, 0, "r"),
                (-1, 2, 0, "r"),
                (-1, 2, 1, "r"),
                (-1, 2, 1, "r"),
                (-1, 1, 1, "w"),
                (-1, 1, 1, "w"),
                (-1, 0, 1, "w"),
                (-1, 0, 1, "w"),
                (-1, 1, 0, "w"),
                (-1, 1, 0, "w"),
                (-1, 2, 1, "r"),
                (-1, 0, 1, "w"),
                (-1, 0, 1, "r"),
                (-1, 0, 1, "w"),
                (-1, 0, 1, "w"),
                (-1, 0, 1, "w"),
                (-1, 0, 1, "w"),
                (-1, 1, 1, "w"),
                (-1, 0, 0, "r"),
                (-1, 1, 1, "w"),
                (-1, 2, 0, "r"),
                (-1, 2, 0, "r"),
                (-1, 2, 0, "r"),
                (-1, 2, 0, "r"),
                (-1, 2, 0, "r"),
                (-1, 2, 0, "r"),
                (-1, 2, 0, "r"),
                (-1, 2, 0, "r"),
                (-1, 1, 1, "w"),
                (-1, 1, 1, "w"),
                (-1, 1, 1, "w"),
                (-1, 1, 1, "w"),
                (-1, 0, 0, "r"),
                (-1, 0, 0, "r"),
                (-1, 0, 0, "w"),
                (-1, 0, 0, "w"),
                (-1, 0, 0, "w"),
                (-1, 0, 0, "w"),
                (-1, 0, 0, "w"),
                (-1, 0, 0, "w"),
                (-1, 0, 0, "w"),
                (-1, 1, 0, "w"),
                (-1, 1, 0, "w"),
                (-1, 2, 1, "r"),
                (-1, 2, 1, "r"),
            ]
        )

        spatial = Preset(
            id=-1,
            name="Localidad Espacial",
            ram=500,
            program_size=2000,
            page_size=50,
            program_count=8,
            reference_trace=[
                (-1, 7, 9, "w"),
                (-1, 7, 8, "w"),
                (-1, 7, 7, "w"),
                (-1, 4, 2, "w"),
                (-1, 4, 1, "r"),
                (-1, 7, 8, "r"),
                (-1, 5, 6, "w"),
                (-1, 5, 6, "r"),
                (-1, 7, 7, "w"),
                (-1, 7, 7, "r"),
                (-1, 4, 3, "r"),
                (-1, 4, 3, "r"),
                (-1, 4, 3, "r"),
                (-1, 4, 1, "r"),
                (-1, 2, 0, "r"),
                (-1, 2, 0, "r"),
                (-1, 2, 2, "w"),
                (-1, 5, 5, "r"),
                (-1, 5, 4, "r"),
                (-1, 5, 4, "w"),
                (-1, 5, 4, "w"),
                (-1, 2, 0, "r"),
                (-1, 2, 1, "w"),
                (-1, 2, 2, "w"),
                (-1, 7, 10, "w"),
                (-1, 7, 6, "w"),
                (-1, 7, 7, "w"),
                (-1, 7, 11, "w"),
                (-1, 2, 6, "w"),
                (-1, 2, 2, "w"),
                (-1, 2, 3, "w"),
                (-1, 2, 4, "w"),
                (-1, 2, 5, "w"),
                (-1, 5, 5, "r"),
                (-1, 5, 4, "r"),
                (-1, 5, 5, "r"),
                (-1, 5, 4, "r"),
                (-1, 5, 5, "r"),
                (-1, 5, 3, "r"),

            ]
        )

        big_memory = Preset(
            id=-1,
            name="Memoria Grande",
            ram=40960,
            program_size=81920,
            page_size=4096,
            program_count=5,
            reference_trace=[
                (-1, 2, 3, "r"),
                (-1, 2, 5, "r"),
                (-1, 3, 3, "r"),
                (-1, 3, 4, "r"),
                (-1, 2, 3, "r"),
                (-1, 2, 4, "r"),
                (-1, 3, 5, "r"),
                (-1, 0, 7, "w"),
                (-1, 0, 1, "r"),
                (-1, 3, 3, "r"),
                (-1, 3, 8, "r"),
                (-1, 0, 3, "w"),
                (-1, 0, 4, "r"),
                (-1, 3, 7, "r"),
                (-1, 0, 2, "w"),
                (-1, 0, 2, "r"),
                (-1, 0, 2, "w"),
                (-1, 0, 2, "r"),
                (-1, 0, 7, "w"),
                (-1, 0, 4, "r"),
                (-1, 4, 7, "w"),
                (-1, 4, 8, "r"),
                (-1, 2, 7, "r"),
                (-1, 2, 8, "r"),
                (-1, 4, 6, "w"),
                (-1, 4, 7, "w"),
                (-1, 0, 1, "r"),
                (-1, 0, 3, "w"),
                (-1, 4, 7, "w"),
                (-1, 4, 8, "w"),
            ]
        )

        little_memory = Preset(
            id=-1,
            name="Memoria Pequeña",
            ram=20480,
            program_size=81920,
            page_size=4096,
            program_count=5,
            reference_trace=[
                (-1, 2, 3, "r"),
                (-1, 2, 5, "r"),
                (-1, 3, 3, "r"),
                (-1, 3, 4, "r"),
                (-1, 2, 3, "r"),
                (-1, 2, 4, "r"),
                (-1, 3, 5, "r"),
                (-1, 0, 7, "w"),
                (-1, 0, 1, "r"),
                (-1, 3, 3, "r"),
                (-1, 3, 8, "r"),
                (-1, 0, 3, "w"),
                (-1, 0, 4, "r"),
                (-1, 3, 7, "r"),
                (-1, 0, 2, "w"),
                (-1, 0, 2, "r"),
                (-1, 0, 2, "w"),
                (-1, 0, 2, "r"),
                (-1, 0, 7, "w"),
                (-1, 0, 4, "r"),
                (-1, 4, 7, "w"),
                (-1, 4, 8, "r"),
                (-1, 2, 7, "r"),
                (-1, 2, 8, "r"),
                (-1, 4, 6, "w"),
                (-1, 4, 7, "w"),
                (-1, 0, 1, "r"),
                (-1, 0, 3, "w"),
                (-1, 4, 7, "w"),
                (-1, 4, 8, "w"),
            ]
        )

        big_page_size = Preset(
            id=-1,
            name="Tamaño de página grande",
            ram=24576,
            program_size=81920,
            page_size=8192,
            program_count=5,
            reference_trace=[
                (-1, 2, 3, "r"),
                (-1, 2, 5, "r"),
                (-1, 3, 3, "r"),
                (-1, 3, 4, "r"),
                (-1, 2, 3, "r"),
                (-1, 2, 4, "r"),
                (-1, 3, 5, "r"),
                (-1, 0, 7, "w"),
                (-1, 0, 1, "r"),
                (-1, 3, 3, "r"),
                (-1, 3, 8, "r"),
                (-1, 0, 3, "w"),
                (-1, 0, 4, "r"),
                (-1, 3, 7, "r"),
                (-1, 0, 2, "w"),
                (-1, 0, 2, "r"),
                (-1, 0, 2, "w"),
                (-1, 0, 2, "r"),
                (-1, 0, 7, "w"),
                (-1, 0, 4, "r"),
                (-1, 4, 7, "w"),
                (-1, 4, 8, "r"),
                (-1, 2, 7, "r"),
                (-1, 2, 8, "r"),
                (-1, 4, 6, "w"),
                (-1, 4, 7, "w"),
                (-1, 0, 1, "r"),
                (-1, 0, 3, "w"),
                (-1, 4, 7, "w"),
                (-1, 4, 8, "w"),
            ]
        )

        little_page_size = Preset(
            id=-1,
            name="Tamaño de página pequeño",
            ram=24576,
            program_size=81920,
            page_size=4096,
            program_count=5,
            reference_trace=[
                (-1, 2, 3, "r"),
                (-1, 2, 5, "r"),
                (-1, 3, 3, "r"),
                (-1, 3, 4, "r"),
                (-1, 2, 3, "r"),
                (-1, 2, 4, "r"),
                (-1, 3, 5, "r"),
                (-1, 0, 7, "w"),
                (-1, 0, 1, "r"),
                (-1, 3, 3, "r"),
                (-1, 3, 8, "r"),
                (-1, 0, 3, "w"),
                (-1, 0, 4, "r"),
                (-1, 3, 7, "r"),
                (-1, 0, 2, "w"),
                (-1, 0, 2, "r"),
                (-1, 0, 2, "w"),
                (-1, 0, 2, "r"),
                (-1, 0, 7, "w"),
                (-1, 0, 4, "r"),
                (-1, 4, 7, "w"),
                (-1, 4, 8, "r"),
                (-1, 2, 7, "r"),
                (-1, 2, 8, "r"),
                (-1, 4, 6, "w"),
                (-1, 4, 7, "w"),
                (-1, 0, 1, "r"),
                (-1, 0, 3, "w"),
                (-1, 4, 7, "w"),
                (-1, 4, 8, "w"),
            ]
        )

        self.save_preset(temporal)
        self.save_preset(spatial)
        self.save_preset(big_memory)
        self.save_preset(little_memory)
        self.save_preset(big_page_size)
        self.save_preset(little_page_size)

    def get_presets(self) -> List[Preset]:
        presets = []

        for preset_row in self.presets.itertuples():
            reference_trace = []

            reference_trace_condition = self.presets_reference_trace["preset_id"] == preset_row.Index
            filtered_reference_trace = self.presets_reference_trace[reference_trace_condition]
            for reference_trace_row in filtered_reference_trace.itertuples():
                reference_trace.append(
                    (
                        reference_trace_row.Index,
                        reference_trace_row.pid,
                        reference_trace_row.page,
                        reference_trace_row.mode
                    )
                )

            presets.append(
                Preset(
                    id=preset_row.Index,
                    name=preset_row.name,
                    ram=preset_row.ram,
                    program_size=preset_row.program_size,
                    page_size=preset_row.page_size,
                    program_count=preset_row.program_count,
                    reference_trace=reference_trace
                )
            )

        return presets

    def get_preset(self, preset_id: Optional[int] = None, preset_name: Optional[str] = None) -> Optional[Preset]:
        preset = None

        try:
            if preset_id:
                preset = self.presets.loc[preset_id]
            elif preset_name:
                condition = self.presets["name"] == preset_name
                preset = self.presets.loc[condition]

                if not preset.empty:
                    preset = preset.iloc[0]
                else:
                    return None
            else:
                return None
        except KeyError:
            return None

        preset_id = preset.name

        preset_reference_trace = self.presets_reference_trace[
            self.presets_reference_trace["preset_id"] == preset_id
            ]

        reference_trace = []

        for index, reference_trace_row in preset_reference_trace.iterrows():
            reference_trace.append(
                (
                    reference_trace_row.name,
                    reference_trace_row["pid"],
                    reference_trace_row["page"],
                    reference_trace_row["mode"],
                )
            )

        return Preset(
            id=preset_id,
            name=preset["name"],
            ram=preset["ram"],
            program_size=preset["program_size"],
            page_size=preset["page_size"],
            program_count=preset["program_count"],
            reference_trace=reference_trace,
        )

    def save_preset(self, preset: Preset) -> tuple[Optional[Preset], Optional[str]]:
        new_name = preset.name
        name_check = self.presets[self.presets["name"] == new_name]

        if not name_check.empty and name_check.index[0] != preset.id:
            error_message = f"El nombre '{new_name}' ya existe para otro Preset."
            return None, error_message

        old_preset_id = preset.id
        if preset.id == -1:
            old_preset_id = -1
            max_id = self.presets.index.max()
            if pandas.isna(max_id):
                max_id = 0

            preset.id = max_id + 1
            preset.id = int(preset.id)

        self.presets.loc[preset.id,
        ["name", "ram", "program_size", "page_size", "program_count"]
        ] = [
            preset.name,
            preset.ram,
            preset.program_size,
            preset.page_size,
            preset.program_count
        ]

        reference_trace = preset.reference_trace
        new_rows_trace = []

        max_trace_id = self.presets_reference_trace.index.max()
        if pandas.isna(max_trace_id):
            max_trace_id = 0

        for reference_id, pid, page, mode in reference_trace:
            if reference_id >= 0:
                try:
                    self.presets_reference_trace.loc[reference_id, ["preset_id", "pid", "page", "mode"]] = [
                        preset.id,
                        pid,
                        page,
                        mode
                    ]
                except KeyError:
                    raise KeyError("Reference trace entry not found")
            else:
                max_trace_id += 1
                new_rows_trace.append({
                    "id": max_trace_id,
                    "preset_id": preset.id,
                    "pid": pid,
                    "page": page,
                    "mode": mode,
                })

        if new_rows_trace:
            new_rows_df = pandas.DataFrame(new_rows_trace).set_index("id")
            new_rows_df.index.name = "id"
            self.presets_reference_trace = pandas.concat([self.presets_reference_trace, new_rows_df])

        self.presets.to_csv(self.root_file, index=True)
        self.presets_reference_trace.to_csv(self.trace_file, index=True)

        fresh_preset_id = preset.id
        preset.id = old_preset_id
        return self.get_preset(fresh_preset_id), None

    def delete_preset(self, preset_id: int):
        try:
            self.presets.drop(labels=preset_id, inplace=True)
        except KeyError:
            return

        mask_to_delete = (self.presets_reference_trace["preset_id"] == preset_id)
        indices_to_delete = self.presets_reference_trace[mask_to_delete].index

        if not indices_to_delete.empty:
            self.presets_reference_trace.drop(labels=indices_to_delete, inplace=True)

        self.presets.to_csv(self.root_file, index=True)
        self.presets_reference_trace.to_csv(self.trace_file, index=True)


presets_central = PresetsCentral(root_file="data/presets.csv", trace_file="data/presets_reference_trace.csv")
