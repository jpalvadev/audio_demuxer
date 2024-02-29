# def set_source():
#     source = filedialog.askopenfilename(
#         title="Select audio file",
#         filetypes=constants.FILETYPES,
#     )
#     if not source:
#         return
#     global_vars["source"] = source
#     source_selected_label.set_text(global_vars["source"])
#     check_paths()


# def set_output():
#     output = filedialog.askdirectory(
#         title="Select output directory")
#     if not output:
#         return
#     global_vars["output"] = output
#     output_selected_label.set_text(global_vars["output"])
#     check_paths()


# def show_bitrate_menu():
#     mp3_bitrate_title_label.grid(row=8, column=5, columnspan=2, sticky="ew")
#     mp3_bitrate_menu.grid(row=8, column=7, columnspan=1, sticky="ew")


# def hide_bitrate_menu():
#     mp3_bitrate_title_label.grid_forget()
#     mp3_bitrate_menu.grid_forget()


# def show_jobs_spinbox():
#     jobs_title_label.grid(row=9, column=10, columnspan=1, sticky="w")
#     jobs_spinbox.grid(row=9, column=11, columnspan=2, sticky="ew")


# def hide_jobs_spinbox():
#     jobs_title_label.grid_forget()
#     jobs_spinbox.grid_forget()


# def check_paths():
#     if not global_vars["source"] or not global_vars["output"]:
#         separate_btn.configure(**constants.DISABLED_BTN_STYLE)
#     else:
#         separate_btn.configure(**constants.DEFAULT_BTN_STYLE)


# def update_gui():
#     if global_vars["output_format"] == "MP3":
#         show_bitrate_menu()
#     else:
#         hide_bitrate_menu()

#     if global_vars["device"] == "CPU":
#         show_jobs_spinbox()
#     else:
#         hide_jobs_spinbox()


# def update_global_vars(choice, key):
#     global_vars[key] = choice
#     update_gui()

def set_progress_bar(position, value):
    pass
