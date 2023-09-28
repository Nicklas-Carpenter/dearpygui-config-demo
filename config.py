#!/usr/bin/env python3

from tkinter import HORIZONTAL
import dearpygui.dearpygui as dpg

# Return a new string that is _str padded with spaces, if necessary until it is
# at least _len characters long
def right_pad_str(_str, _len):
  return _str + " " * max(0, _len - len(_str))

# Given a group a strings, finds the longest string and returns a dictionary
# mapping each string in the original group to a version of itself that is
# padded to be as long as the longest string in the original group.
def justify_str_group(*strs):
  justified = {}

  max_len_in_group = 0
  for _str in strs:
    if len(_str) > max_len_in_group:
      max_len_in_group =  len(_str)
  for _str in strs:
    justified[_str] = right_pad_str(_str, max_len_in_group)

  return justified 

# Creat context before we do any with DearPyGui. Depending on the the action,
# we may segfault if the context doesn't exist.
dpg.create_context()

### General callback functions

# A callback function called that enables/disables the given item when the
# toggle state of the sender changes. Usually used for checkboxes.
def cb_handle_enable_state_on_toggle(_, enabled, item):
  if enabled:
    dpg.enable_item(item)
  else:
    dpg.disable_item(item)

with dpg.item_handler_registry(tag="show_item_on_click") as handler:
  def cb_show_item_on_click(_, click_event_data):
    # I couldn't find this in the documentation, but was able to determine
    # through testing that the second item of the 'click_event_data' tuple is
    # the id of the element that was clicked. This is why we document things
    # people!
    clicked_item = click_event_data[1]
    target = dpg.get_item_user_data(clicked_item) 
    dpg.show_item(target)

  dpg.add_item_clicked_handler(callback=cb_show_item_on_click)

def cb_handle_select_one_file(_, file_selection_data, write_loc):
  # We iterate through all the selected files. Since we didn't specify
  # multi-select, there should be exactly either 0 or 1 files i the list.
  # If there are 0, assume the user is effective cancelling (not choosing) and
  # do nothing.
  selected_files = list(file_selection_data["selections"].values())
  if len(selected_files) == 0:
    return
  dpg.set_value(write_loc, selected_files[0])

### Start creating GUI ###

dpg.create_viewport(title="Config Editor", width=1000, height=700)#,
                    #max_width=700, min_width=700, max_height=700,
                    #min_height=700)

with dpg.window(label="", width=1000, height=700, no_resize=True, no_move=True,
                no_collapse=True, no_title_bar=True):
  ### Section for configuring operation mode ###
  with dpg.collapsing_header(label="Operation Mode"):
    dpg.add_radio_button(["Fully Intrisinc", "Simulate Hardware",
                          "Fully Simulated"], default_value="Fully Intrinsic")

  ### Section for configuring fitness function and its parameters ###
  with dpg.collapsing_header(label="Fitness"):
    fit_justified_strs = justify_str_group("Variance Weight: ",
                                            "Pulse Weight: ",
                                            "Combination Type: ",
                                            "Oscillator Frequency: ")

    # A callback function called everytime the value chosen for the fitness
    # function changes. Since each fitness function has different parameters
    # (or at least different names for the parameters), this function ensures
    # that the config application shows only the parameter for the currently
    # selected fitness function
    def cb_update_fit_fn(sender, fitness_function):
      dpg.delete_item("fit_fn_param")
      
      if fitness_function == "Combined":
        with dpg.group(tag="fit_fn_param",
                        before="fit_fn_param_anchor"):
          with (dpg.group(horizontal=True)):
            dpg.add_text(fit_justified_strs["Combination Type: "])
            dpg.add_radio_button(["Add", "Mult"], horizontal=True)
          
          with (dpg.group(horizontal=True)):
            dpg.add_text(fit_justified_strs["Variance Weight: "])
            dpg.add_slider_float(min_value=0, max_value=5.0, clamped=True)

          with (dpg.group(horizontal=True)):
            dpg.add_text(fit_justified_strs["Pulse Weight: "])
            dpg.add_slider_float(min_value=0, max_value=5.0, clamped=True)

    dpg.add_text("Fitness Function:")
    dpg.add_radio_button(["Variance", "Pulse", "Combined"],
                          default_value="Variance", callback=cb_update_fit_fn,
                          horizontal=True)

    dpg.add_separator(tag="fit_fn_param_anchor")

    with dpg.group(horizontal=True):
      dpg.add_text(fit_justified_strs["Oscillator Frequency: "])
      dpg.add_input_int(min_value=1, min_clamped=True, max_value=1000000,
                        max_clamped=True, default_value=1000)

    
  ### Section for configuring genetic algorithm parameters ###
  with dpg.collapsing_header(label="Genetic Algorithm"):
    ga_justified_strs = justify_str_group("Population Size: ",
                                        "Mutation Probability: ",
                                        "Crossover Probability: ",
                                        "Elitism Fraction: ")

    with dpg.group(horizontal=True):
      dpg.add_text(ga_justified_strs["Population Size: "])
      dpg.add_input_int(min_value=2, min_clamped=True, default_value=50)

    dpg.add_separator()

    with dpg.group(horizontal=True):
      dpg.add_text(ga_justified_strs["Mutation Probability: "])
      dpg.add_slider_float(min_value=0, max_value=1.0, clamped=True)

    with dpg.group(horizontal=True):
      dpg.add_text(ga_justified_strs["Crossover Probability: "])
      dpg.add_slider_float(min_value=0, max_value=1.0, clamped=True)

    with dpg.group(horizontal=True):
      dpg.add_text(ga_justified_strs["Elitism Fraction: "])
      dpg.add_slider_float(min_value=0, max_value=1.0, clamped=True)

    dpg.add_separator()

    with dpg.table(header_row=False):
      dpg.add_table_column()
      dpg.add_table_column()

      with dpg.table_row():
        with dpg.table_cell():
          dpg.add_text("Selection Type:")
          dpg.add_radio_button(["Single Elite", "Fractional Elite",
                                "Classic Tournament",
                                "Fitness Proportional", "Rank Proportional"],
                                default_value="Fitness Proportional")

        with dpg.table_cell():
          dpg.add_text("Diversity Measure:")
          dpg.add_radio_button(["None", "Unique", "Hamming Distance"],
                                default_value="Hamming Distance")

    dpg.add_separator()

    stp_justified_strs = justify_str_group("Stop after generation: ",
                                           "Stop after reaching fitness value: ")

    with dpg.group(horizontal=True):
      dpg.add_checkbox(label=stp_justified_strs["Stop after generation: "],
                        callback=cb_handle_enable_state_on_toggle,
                        user_data="gen_max", default_value=True)
      dpg.add_input_int(min_value=2, min_clamped=True, default_value=500,
                        tag="gen_max")

    with dpg.group(horizontal=True):
      dpg.add_checkbox(label=stp_justified_strs["Stop after reaching fitness value: "],
                        callback=cb_handle_enable_state_on_toggle,
                        user_data="fitness_target")
      dpg.add_input_int(min_value=2, min_clamped=True, default_value=1000,
                        enabled=False, tag="fitness_target")

  ### Section for configuring initialization mode ###
  with dpg.collapsing_header(label="Initialization"):
    # A callback function called everytime the initialization mode changes. It's
    # responsible for showing/hiding the randomization parameters everytime the
    # "Randomize" option is selected/deselected.
    def cb_handle_init_mode_change(sender, init_mode):
      if init_mode == "Randomize":
        with dpg.group(horizontal=True, tag="randomize_params",
                        before="randomize_params_anchor"):
          dpg.add_text("Randomize: ")
          dpg.add_combo(["until pulse threshold", "until variance threshold",
                           "once"], default_value="once")
      else:
        dpg.delete_item("randomize_params")

    with dpg.group():
      dpg.add_text("Initialization Mode:")
      dpg.add_radio_button(["Clone from seed", "Clone from seed and mutate",
                            "Randomize", "Use existing population"],
                            callback=cb_handle_init_mode_change,
                            default_value="Randomize")

    with dpg.group(horizontal=True, tag="randomize_params"):
      dpg.add_text("Randomize: ")
      dpg.add_combo(["until pulse threshold", "until variance threshold",
                       "once"], default_value="once")
    dpg.add_spacer(tag="randomize_params_anchor")
  
  ### Section for configuring logging and output ###
  with dpg.collapsing_header(label="Logging and Output"):
    outp_justified_strs = justify_str_group("Log level: ", "Log to file: ",
                                          "Save plots to: ",
                                          "Save Output to: ",
                                          "Save .asc files to: ",
                                          "Save .bin files to: ",
                                          "Save MCU data to: ",
                                          "Analysis directory: ",
                                          "Populations source: ")

    with dpg.group(horizontal=True):
      dpg.add_text(outp_justified_strs["Log level: "])
      dpg.add_slider_int(min_value=0, max_value=4, default_value=0)

    dpg.add_separator()

    with dpg.group(horizontal=True):
      dpg.add_checkbox(label=outp_justified_strs["Log to file: "],
                        default_value=True)
      dpg.add_input_text(readonly=True, tag="log_file_display",
                          user_data="log_file_selector")
      dpg.bind_item_handler_registry("log_file_display", "show_item_on_click")

      # NOTE: If modal=False, then if the user clicks outside the file dialog,
      # the parent window will become active and the dialog will be hidden
      # behind it. If we disable movement of the parent window, the file dialog
      # will effectively be lost for good, so in that case we should set
      # modal=True
      with dpg.file_dialog(show=False, directory_selector=False, modal=True,
                            width=500, height=300, tag="log_file_selector",
                            callback=cb_handle_select_one_file,
                            user_data="log_file_display"):
        dpg.add_file_extension(".*")

    with dpg.group(horizontal=True):
      dpg.add_checkbox(label=outp_justified_strs["Save plots to: "], 
                        callback=cb_handle_enable_state_on_toggle,
                        user_data="plot_file_display", default_value=True)
      dpg.add_input_text(readonly=True, tag="plot_file_display",
                          user_data="plot_file_selector")
      dpg.bind_item_handler_registry("plot_file_display", "show_item_on_click")

      with dpg.file_dialog(show=False, directory_selector=True, modal=True,
                            width=500, height=300, tag="plot_file_selector",
                            callback=cb_handle_select_one_file,
                            user_data="plot_file_display"):
        dpg.add_file_extension(".*")

    dpg.add_separator()

    # Non-optional output directories
    items = ["Save Output to: ", "Save .asc files to: ",
             "Save .bin files to: ", "Save MCU data to: ",
             "Analysis directory: ", "Populations source: "]
    for item in items:
      with dpg.group(horizontal=True):
        dpg.add_text(outp_justified_strs[item])
        dpg.add_input_text(readonly=True, tag=f"{item} display",
                            user_data=f"{item} selector")
        dpg.bind_item_handler_registry(f"{item} display", "show_item_on_click")
        with dpg.file_dialog(show=False, directory_selector=True, modal=True,
                              width=500, height=300, tag=f"{item} selector",
                              user_data=f"{item} display",
                              callback=cb_handle_select_one_file):
          dpg.add_file_extension(".*")

  ## Section for configuring system parameters
  with dpg.collapsing_header(label="System"):
    with dpg.group(horizontal=True):
      dpg.add_text("MCU USB device: ")
      dpg.add_input_text(readonly=True, tag="device_file_display",
                          user_data="device_file_selector")
      dpg.bind_item_handler_registry("device_file_display", "show_item_on_click")

      # NOTE: If modal=False, then if the user clicks outside the file dialog,
      # the parent window will become active and the dialog will be hidden
      # behind it. If we disable movement of the parent window, the file dialog
      # will effectively be lost for good, so in that case we should set
      # modal=True
      with dpg.file_dialog(show=False, directory_selector=False, modal=True,
                            width=500, height=300, tag="device_file_selector",
                            callback=cb_handle_select_one_file,
                            user_data="device_file_display"):
        dpg.add_file_extension(".*")

  ## Section for configuring hardware parameters
  with dpg.collapsing_header(label="Hardware"):
    hw_justified_strs = justify_str_group("Baud rate: ", "MCU read timeout: ",
                                          "FPGA routing: ")
    with dpg.group(horizontal=True):
      dpg.add_text(hw_justified_strs["Baud rate: "])
      dpg.add_combo([9600, 14400, 19200, 38400, 57600, 115200],
                    default_value=115200)
    with dpg.group(horizontal=True):
      dpg.add_text(hw_justified_strs["MCU read timeout: "])
      dpg.add_input_float(min_value=1.0, min_clamped=True, default_value=1.1,
                          step=0.1)

    dpg.add_separator()

    with dpg.group(horizontal=True):
      dpg.add_text(hw_justified_strs["FPGA routing: "])
      dpg.add_radio_button(["MOORE", "NEWSE"], default_value="MOORE",
                            horizontal=True)
    dpg.add_text("Accessed columns: ")
    with dpg.table(header_row=False):
      for i in range (9):
        dpg.add_table_column()

      idx = 0 
      for i in range(6):
        with dpg.table_row():
          for j in range(9):
            dpg.add_selectable(label=idx)  
            idx += 1

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
