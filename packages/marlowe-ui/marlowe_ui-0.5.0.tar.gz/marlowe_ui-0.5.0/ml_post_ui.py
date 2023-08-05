#!/usr/bin/env python

import re
import logging
import traceback

import tkinter as tk
import tkinter.ttk

import marlowe_ui.tktool.askfilename
import marlowe_ui.tktool.codedoptionmenu
import marlowe_ui.logconsole

import marlowe_ui.postprocess.dumper as old_dumper
import marlowe_ui.postprocess_lark.dumper as dumper

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    app = tk.Tk()

    # input file chooser
    labelframe = tk.LabelFrame(app, text='Input Filename')
    labelframe.pack(fill=tk.X)

    filepath = marlowe_ui.tktool.askfilename.OpenFileName(
        labelframe,
        diagfiletypes=[('Marlowe output', '*.lst'), ('All', '*')])
    filepath.pack(fill=tk.X)

    def runbutton():
        try:
            inputf = filepath.get()
            logger.info('input file: {}'.format(inputf))
            if not inputf:
                raise Exception('input file is Null')

            # generate output dirname
            output = re.sub('\.lst$', '.post', inputf)
            logger.info('output directory: {}'.format(output))

            if inputf == output:
                raise Exception('input and output have same name,'
                                'input file should have ".lst" suffix, currently')
            with open(inputf, 'rt') as f:
                if use_old_parser_var.get():
                    logger.info('Expand using old inline parser')
                    p = old_dumper.Parser(outputdir=output)
                    p.parse(f)
                else:
                    logger.info('Expand options')
                    dumper.run(f, outputdir=output,
                            config_dump_text_blocks = not skip_verbose_textblockout_var.get(),
                            config_cascade_table_output = cascade_table_output.get())
                    logger.info(f'--skip-verbose-textblock-output: {skip_verbose_textblockout_var.get()}')
                    logger.info(f'--cascade-table-output: {cascade_table_output.get()}')
                    logger.info('start expansion')
            logger.info('finished.')
        except Exception as e:
            logger.error(str(e), exc_info=True)
        logger.info('ready')

    # run button
    button = tk.Button(app, text='Expand Data', command=runbutton)
    button.pack()

    # tab frame
    tab = tkinter.ttk.Notebook(app)
    tab.pack(expand=True, fill=tk.BOTH)

    # tab 1 - msgbox
    logtext = tk.scrolledtext.ScrolledText(app)
    logtext.pack(expand=True, fill=tk.BOTH)
    tab.add(logtext, text='Message')

    # tab 2 - options
    option = tk.Frame(app, padx=10, pady=10)
    tab.add(option, text='Options')

    # logging level
    logging_frame = tk.LabelFrame(option, text='Logging')
    logging_level_label = tk.Label(logging_frame, text='logging level')
    logging_level_var = tk.StringVar(logging_frame, 'WARNING')

    def on_logging_level(v):
        # dumper.logger.setLevel(logging.getLevelName(v))
        # old_dumper.logger.setLevel(logging.getLevelName(v))

        logging.getLogger().setLevel(v)

        logger.info(f'default logging level is {v}')

        # print all loggers
        # for name in logging.root.manager.loggerDict:
        #     lo = logging.getLogger(name)
        #     print(name, lo.getEffectiveLevel(), lo.propagate)

    logging_level = tk.OptionMenu(logging_frame, logging_level_var,
            'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', command=on_logging_level)
    logging_level_label.pack(side=tk.LEFT)
    logging_level.pack(side=tk.LEFT)

    logging_frame.pack(anchor=tk.W)

    # control option
    output_ctrl_frame = tk.LabelFrame(option, text='Output control')
    skip_verbose_textblockout_var = tk.BooleanVar(output_ctrl_frame, False)
    skip_verbose_textblockout = tk.Checkbutton(output_ctrl_frame,
            variable=skip_verbose_textblockout_var,
            text='Skip output of verbose text block')
    cascade_table_label = tk.Label(output_ctrl_frame, text='Output form for large cascade data tables:')
    cascade_table_output = marlowe_ui.tktool.codedoptionmenu.CodedOptionMenu(
            output_ctrl_frame,
            options = [
                ('BUNDLE', 'BUNDLE: output as <root>/xxx_all.csv'),
                ('SEPARATE', 'SEPARATE: output as <root>/<each cascade>/xxx.csv'), 
                ('BOTH', 'BOTH: BUNDLE and SEPARATE')])
    cascade_table_output.set('BUNDLE')
    skip_verbose_textblockout.pack(anchor=tk.W) 
    cascade_table_label.pack(anchor=tk.W)
    cascade_table_output.pack(anchor=tk.E) 

    output_ctrl_frame.pack(anchor=tk.W, pady=5)

    # use old parser
    def on_use_old_parser():
        v = use_old_parser_var.get()
        if v:
            state = tk.DISABLED
        else:
            state = tk.NORMAL

        for c in output_ctrl_frame.winfo_children():
            c.config(state=state)

    use_old_parser_var = tk.BooleanVar(option, False)
    use_old_parser = tk.Checkbutton(option,
            variable=use_old_parser_var,
            text='use old inline parser',
            command=on_use_old_parser)

    use_old_parser.pack(anchor=tk.W, pady=5)


    # bind logging handler
    h = marlowe_ui.logconsole.LogConsoleHandler(logtext)
    h.setFormatter(logging.Formatter('%(levelname)s %(name)s: %(message)s'))
    logging.getLogger().addHandler(h)
    logging.getLogger().setLevel('WARNING')

    # initial logging message
    logger.setLevel(logging.INFO)
    logger.info('ml_post_ui is ready. Select input file to be expanded')

    app.mainloop()
