# `bulkdgd reduction`

This command allows the user to perform dimensionality reduction analyses on sets of data points (such as latent representations generated by the bulkDGD model).

`bulkdgd reduction` has four sub-commands:

* `bulkdgd reduction pca` performs a principal component analysis (PCA).
* `bulkdgd reduction kpca` performs a kernel principal component analysis (KPCA).
* `bulkdgd reduction mds` performs a multidimensional scaling analysis (MDS).
* `bulkdgd reduction tsne` performs a t-distributed stochastic neighbor embedding analysis (t-SNE).

All sub-commands expect a CSV file containing a data frame with the data points as input, where each row represents a data point. Each column should contain either the data point values along a dimension or additional information about the data points.

The sub-commands produce three outputs:

* A CSV file containing a data frame with the results of the dimensionality reduction.
* A PKL file containing the fitted model used to perform the dimensionality reduction
* A file containing a scatter plot of the results of the dimensionality reduction.

The sub-commands can also take a configuration file as input, specifying the plot's aesthetics and output format. If not provided, the default configuration file for the analysis performed by the sub-command is used to generate the plot. These default configuration files can be found in `bulkDGD/configs/plotting` and are named after the analyses they refer to.

## Parallelization

If the command is parallelized over several input files or configuration files, each is assumed to be identically named and placed in a different directory. The paths to such directories must be specified using the `-ds`, `--dirs` option (see the full description in the [Parallelization options](#parallelization-options) section below) and must be relative to the specified working directory (`-d`, `--work-dir` option).

You can also run the command with the same input file using different configuration files and vice versa.

In these cases, the files that vary among the runs must be placed in different directories and referenced by their corresponding options by name (not path).

In contrast, the input/configuration files that stay the same among runs may be placed anywhere and referenced by their corresponding options using their absolute path or path relative to the specified working directory.

The output and log files for each run will be written in the directory where the corresponding input/configuration files were placed. If the command is not parallelized, these files will be written in the working directory.

## Command lines

```
dgd reduction pca [-h] -id INPUT_DATA [-im INPUT_MODEL] [-ic INPUT_COLUMNS] [-oa OUTPUT_ANALYSIS] [-om OUTPUT_MODEL] [-op OUTPUT_PLOT] [-cd CONFIG_FILE_DIM_RED] [-cp CONFIG_FILE_PLOT] [-fp FILL_POS_INF] [-fn FILL_NEG_INF] [-gc GROUPS_COLUMN] [-gr GROUPS] [-pg] [-d WORK_DIR] [-lf LOG_FILE] [-lc] [-v] [-vv] [-p] [-n N_PROC] [-ds DIRS [DIRS ...]]
```

```
dgd reduction kpca [-h] -id INPUT_DATA [-im INPUT_MODEL] [-ic INPUT_COLUMNS] [-oa OUTPUT_ANALYSIS] [-om OUTPUT_MODEL] [-op OUTPUT_PLOT] [-cd CONFIG_FILE_DIM_RED] [-cp CONFIG_FILE_PLOT] [-fp FILL_POS_INF] [-fn FILL_NEG_INF] [-gc GROUPS_COLUMN] [-gr GROUPS] [-pg] [-d WORK_DIR] [-lf LOG_FILE] [-lc] [-v] [-vv] [-p] [-n N_PROC] [-ds DIRS [DIRS ...]]
```

```
dgd reduction mds [-h] -id INPUT_DATA [-im INPUT_MODEL] [-ic INPUT_COLUMNS] [-oa OUTPUT_ANALYSIS] [-om OUTPUT_MODEL] [-op OUTPUT_PLOT] [-cd CONFIG_FILE_DIM_RED] [-cp CONFIG_FILE_PLOT] [-fp FILL_POS_INF] [-fn FILL_NEG_INF] [-gc GROUPS_COLUMN] [-gr GROUPS] [-pg] [-d WORK_DIR] [-lf LOG_FILE] [-lc] [-v] [-vv] [-p] [-n N_PROC] [-ds DIRS [DIRS ...]]
```

```
dgd reduction tsne [-h] -id INPUT_DATA [-im INPUT_MODEL] [-ic INPUT_COLUMNS] [-oa OUTPUT_ANALYSIS] [-om OUTPUT_MODEL] [-op OUTPUT_PLOT] [-cd CONFIG_FILE_DIM_RED] [-cp CONFIG_FILE_PLOT] [-fp FILL_POS_INF] [-fn FILL_NEG_INF] [-gc GROUPS_COLUMN] [-gr GROUPS] [-pg] [-d WORK_DIR] [-lf LOG_FILE] [-lc] [-v] [-vv] [-p] [-n N_PROC] [-ds DIRS [DIRS ...]]
```

## Options (all sub-commands)

### Help options

| Option         | Description                     |
| -------------- | ------------------------------- |
| `-h`, `--help` | Show the help message and exit. |

### Input options

| Option                   | Description                                                  |
| ------------------------ | ------------------------------------------------------------ |
| `-id`, `--input-data`    | The input CSV file containing the data frame with the data points. |
| `-im`, `--input-model`   | The input PKL file containing the fitted model on which to project the new data points. |
| `-ic`, `--input-columns` | A comma-separated list of columns or a string representing a pattern matching the columns of interest. These will be the columns considered when performing the dimensionality reduction analysis. By default, all columns are considered. |

### Output files

| Option                     | Description                                                  |
| -------------------------- | ------------------------------------------------------------ |
| `-oa`, `--output-analysis` | The name of the output CSV file containing the results of the dimensionality reduction analysis. The default file name changes according to the sub-command used. |
| `-om`, `--output-model`    | The name of the output pickle file containing the fitted model used to perform the dimensionality reduction analysis. The default file name changes according to the sub-command used. |
| `-op`, `--output-plot`     | The name of the output file containing the plot displaying the results of the dimensionality reduction analysis.  The default file name changes according to the sub-command used. The file format and, therefore, extension are inferred from the `output` section of the configuration file for plotting. |

### Configuration files

| Option                        | Description                                                  |
| ----------------------------- | ------------------------------------------------------------ |
| `-cd`, `--config-file-dimred` | The YAML configuration file specifying the options for the dimensionality reduction analysis. If it is a name without an extension, it is assumed to be the name of a configuration file in `$INSTALLDIR/bulkDGD/configs/dimensionality_reduction`. If not provided, the default configuration file for the analysis performed by the sub-command will be used. |
| `-cp`, `--config-file-plot`   | The YAML configuration file specifying the plot's aesthetics and output format.  If it is a name without an extension, it is assumed to be the name of a configuration file in `$INSTALLDIR/bulkDGD/configs/plotting`. If not provided, the default configuration file for the analysis performed by the sub-command will be used. |

### Pre-processing options

| Option                  | Description                                                  |
| ----------------------- | ------------------------------------------------------------ |
| `-fp`, `--fill-pos-inf` | Replace all positive infinite values with the given value before performing the dimensionality reduction analysis. |
| `-fn`, `--fill-neg-inf` | Replace all negative infinite values with the given value before performing the dimensionality reduction analysis. |

### Plotting options

| Option                       | Description                                                  |
| ---------------------------- | ------------------------------------------------------------ |
| `-gc`, `--groups-column`     | The name/index of the column in the input data frame containing the groups by which the samples will be colored in the output plot. By default, the program assumes that no such column is present. |
| `-gr`, `--groups`            | A comma-separated list of groups whose data points should be plotted. By default, all groups found in the `-gc`, ` --groups-column` column, if passed, will be included in the plot. Data points not belonging to these groups will not be included. However, you can use the `-pg`, `--plot-other-groups` option to plot them using different aesthetics compared to the groups of interest. |
| `-pg`, `--plot-other-groups` | Whether to plot data points from the groups not included in the `-gr`, `--groups` list. The aesthetics to plot these data points should also be defined in the configuration file for plotting. |

### Working directory options

| Option             | Description                                                  |
| ------------------ | ------------------------------------------------------------ |
| `-d`, `--work-dir` | The working directory. The default is the current working directory. |

### Logging options

| Option                    | Description                                                  |
| ------------------------- | ------------------------------------------------------------ |
| `-lf`, `--log-file`       | The name of the log file. The default file name depends on the sub-command. |
| `-lc`, `--log-console`    | Show log messages also on the console.                       |
| `-v`, `--logging-verbose` | Enable verbose logging (INFO level).                         |
| `-vv`, `--logging-debug`  | Enable maximally verbose logging for debugging purposes (DEBUG level). |

### Parallelization options

| Option                | Description                                                  |
| --------------------- | ------------------------------------------------------------ |
| `-p`, `--parallelize` | Whether to run the command in parallel.                      |
| `-n`, `--n-proc`      | The number of processes to start. The default number of processes started is 1. |
| `-ds`, `--dirs`       | The directories containing the input/configuration files. It can be either a list of names or paths, a pattern that the names or paths match, or a plain text file containing the names of or the paths to the directories. If names are given, the directories are assumed to be inside the working directory. If paths are given, they are assumed to be relative to the working directory. |