def write_mecr_mapping_dict(directories, image_mecr_idx_map):
    folder_name = directories["mecr_eqn_idx_maps"]

    for key in image_mecr_idx_map:
        file_name = key.split(".")[0] + ".txt" # key = image_name = 3.jpg     
        file_path = folder_name + file_name

        with open(file_path, "w") as f:
            for eqn_idx in image_mecr_idx_map[key]:
                f.write(eqn_idx + " <==> " + image_mecr_idx_map[key][eqn_idx] + "\n")