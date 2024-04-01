from modules.main_consulting_system import main_get_commerce_df

if __name__ == "__main__":
    main_get_commerce_df(
        commerce="exports",
        frequency="M",
        year_from=2019,
        drop_all_files=True,
        export_raw_concat_df=True        
    )