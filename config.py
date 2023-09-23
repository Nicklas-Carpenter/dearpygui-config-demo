#!/usr/bin/env python3

import dearpygui.dearpygui as dpg

def cb_update_fit_fn(sender, widget_data):
  dpg.delete_item("fit_fn_aux_data")
  
  if widget_data == "Variance":
    with dpg.group():
      dpg.add_text("Variance Weight")
      dpg.add_slider_float(min_value=0, max_value=1.0, clamped=True,
                            tag="fit_fn_aux_data",
                            before="Oscillator Frequency")
  elif widget_data == "Pulse":
    dpg.add_text("Pulse Weight")
    dpg.add_slider_float(min_value=0, max_value=1.0, clamped=True,
                          tag="fit_fn_aux_data",
                          before="Oscillator Frequency")
  elif widget_data == "Combined":
    with dpg.group(tag="fit_fn_aux_data", before="Oscillator Frequency"):
      dpg.add_text("Combination Type:")
      dpg.add_radio_button(["Add", "Mult"], horizontal=True)
                          
  else:
    raise Exception("You broke my app :(")
 

dpg.create_context()
dpg.create_viewport(title="Config Editor", width=700, height=700)

with dpg.window(label="", width=700, height=700):
  with dpg.collapsing_header(label="Operation Mode"):
    dpg.add_radio_button(["Fully Intrisinc", "Simulate Hardware",
                          "Fully Simulated"], default_value="Fully Intrinsic")
  with dpg.collapsing_header(label="Fitness Parameters"):
    dpg.add_text("Fitness Function:")
    dpg.add_radio_button(["Variance", "Pulse", "Combined"],
                          default_value="Variance", callback=cb_update_fit_fn)
    with dpg.group():
      dpg.add_text("Variance Weight:")
      dpg.add_slider_float(min_value=0, max_value=1.0,
                          clamped=True, tag="fit_fn_aux_data")
    with dpg.group(horizontal=True):
      dpg.add_text("Oscillator Frequency")
      dpg.add_input_int(tag="Oscillator Frequency", min_value=1,
                        min_clamped=True, max_value=1000000, max_clamped=True,
                        default_value=1000)
  with dpg.collapsing_header(label="Genetic Algorithm Parameters"):
    dpg.add_input_int(label="Population Size", min_value=2, min_clamped=True,
                      default_value=50)
    dpg.add_slider_float(label="Mutation Probability", min_value=0,
                          max_value=1.0, clamped=True)
    dpg.add_slider_float(label="Crossover Probability", min_value=0,
                          max_value=1.0, clamped=True)
    dpg.add_slider_float(label="Elitism Fraction", min_value=0, max_value=1.0,
                          clamped=True)
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



dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
