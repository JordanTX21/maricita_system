class IDGenerator:

    @staticmethod
    def next_id(df, prefix, pad=3):
        """
        df      : DataFrame leído desde Excel
        prefix  : prefijo del ID (P, C, PED, etc.)
        pad     : cantidad de ceros
        """
        if df.empty:
            return f"{prefix}{'0' * (pad - 1)}1"

        # Extraer parte numérica
        last_id = df["id"].astype(str).str.replace(prefix, "", regex=False)
        last_num = last_id.astype(int).max()

        next_num = last_num + 1
        return f"{prefix}{str(next_num).zfill(pad)}"
