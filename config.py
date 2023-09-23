#!/usr/bin/env python3

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

dpg.create_context()
dpg.create_viewport(title="Config Editor", width=700, height=700,
                    max_width=700, min_width=700, max_height=700,
                    min_height=700)

with dpg.window(label="", width=700, height=700, no_resize=True, no_move=True,
                no_collapse=True, no_title_bar=True):
  ### Section for configuring operation mode ###
  with dpg.collapsing_header(label="Operation Mode"):
    dpg.add_radio_button(["Fully Intrisinc", "Simulate Hardware",
                          "Fully Simulated"], default_value="Fully Intrinsic")

  ### Section for configuring fitness function and its parameters ###

    
  justified_strs = justify_str_group("Variance Weight: ", "Pulse Weight: ",
                                      "Combination Type: ",
                                      "Oscillator Frequency: ")

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
      
      if fitness_function == "Variance":
        with dpg.group(horizontal=True, tag="fit_fn_param",
                        before="fit_fn_param_anchor"):
          dpg.add_text(fit_justified_strs["Variance Weight: "])
          dpg.add_slider_float(min_value=0, max_value=1.0, clamped=True)
      elif fitness_function == "Pulse":
        with dpg.group(horizontal=True, tag="fit_fn_param",
                        before="fit_fn_param_anchor"):
          dpg.add_text(fit_justified_strs["Pulse Weight: "])
          dpg.add_slider_float(min_value=0, max_value=1.0, clamped=True)
      elif fitness_function == "Combined":
        with dpg.group(horizontal=True, tag="fit_fn_param",
                        before="fit_fn_param_anchor"):
          dpg.add_text(fit_justified_strs["Combination Type: "])
          dpg.add_radio_button(["Add", "Mult"], horizontal=True)
      else:
        raise Exception("You broke my app :(")

    dpg.add_text("Fitness Function:")
    dpg.add_radio_button(["Variance", "Pulse", "Combined"],
                          default_value="Variance", callback=cb_update_fit_fn,
                          horizontal=True)

    with dpg.group(horizontal=True, tag="fit_fn_param"):
      dpg.add_text(justified_strs["Variance Weight: "])
      dpg.add_slider_float(min_value=0, max_value=1.0, clamped=True)

    dpg.add_separator(tag="fit_fn_param_anchor")

    with dpg.group(horizontal=True):
      dpg.add_text(justified_strs["Oscillator Frequency: "])
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

    # A callback function called any time the checkbox for the generation stop
    # condition is toggled. Adds/removes the input box for the max number of
    # generations when the checkbox is checked/unchecked.
    def cb_handle_toggle_stop_on_generation(sender, stop_on_generation):
      if stop_on_generation:
        dpg.add_input_int(min_value=2, min_clamped=True, default_value=500,
                          before="gen_max_anchor", tag="gen_max")
      else:
        dpg.delete_item("gen_max")

    with dpg.group(horizontal=True):
      dpg.add_checkbox(label=stp_justified_strs["Stop after generation: "],
                        default_value=True,
                        callback=cb_handle_toggle_stop_on_generation)
      dpg.add_input_int(min_value=2, min_clamped=True, default_value=500,
                        tag="gen_max")
      dpg.add_spacer(tag="gen_max_anchor")

    # A callback function called any time the checkbox for the target fitness
    # stop condition is toggled. Adds/removes the input box for the target
    # fitnes when the checkbox is checked/unchecked.
    def cb_handle_toggle_stop_on_fitness(sender, stop_on_fitness):
      if stop_on_fitness:
        dpg.add_input_int(min_value=2, min_clamped=True, default_value=1000,
                          before="fitness_target_anchor", tag="fitness_target")
      else:
        dpg.delete_item("fitness_target")

    with dpg.group(horizontal=True):
      dpg.add_checkbox(label=stp_justified_strs["Stop after reaching fitness value: "],
                        callback=cb_handle_toggle_stop_on_fitness)
      dpg.add_spacer(tag="fitness_target_anchor")

  ### Section for configuring initialization mode ###

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

  with dpg.collapsing_header(label="Initialization"):
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
  
  ### Section for configuring logging ###
  with dpg.collapsing_header(label="Logging"):
    with dpg.group(horizontal=True):
      dpg.add_text("Log level: ")
      dpg.add_slider_int(min_value=0, max_value=4, default_value=0)

    def cb_handle_select_log_file(sender):
      dpg.show_item("log_file_selector")

    def cb_handle_choose_log_file(send, file_selection_data):
      # We iterate through all the selected files. Since we didn't specify
      # multi-select, there should be exactly one file in the list. If there
      # are no files in the list, something terrible has happened and we can't
      # possibly know how to continue
      selected_files = list(file_selection_data["selections"].values())
      if len(selected_files) == 0:
        raise Exception("Something terrible happened")

      dpg.set_value("log_file_display", selected_files[0])
      
    with dpg.group(horizontal=True):
      dpg.add_text("Log file: ")
      dpg.add_input_text(readonly=True, enabled=False, tag="log_file_display")

      # NOTE: If modal=False, then if the user clicks outside the file dialog,
      # the parent window will become active and the dialog will be hidden
      # behind it. If we disable movement of the parent window, the file dialog
      # will effectively be lost for good, so in that case we should set
      # modal=True
      with dpg.file_dialog(show=False, directory_selector=False, modal=True,
                            width=500, height=300, tag="log_file_selector",
                            callback=cb_handle_choose_log_file):
        dpg.add_file_extension("")
        dpg.add_file_extension(".*")
      dpg.add_button(label="Select", callback=cb_handle_select_log_file)
    

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
