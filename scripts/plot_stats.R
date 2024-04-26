# Set CRAN mirror
options(repos = "https://cloud.r-project.org/")

# Check if ggplot2 package is installed, if not, install it
if (!requireNamespace("ggplot2", quietly = TRUE)) {
  install.packages("ggplot2")
}

# Check if reshape2 package is installed, if not, install it
if (!requireNamespace("reshape2", quietly = TRUE)) {
  install.packages("reshape2")
}

# Load necessary packages
library(ggplot2)
library(reshape2)

# Retrieve command-line arguments
args <- commandArgs(trailingOnly = TRUE)

# Parse command-line arguments
if (length(args) != 4 || !("-i" %in% args) || !("-p" %in% args)) {
  stop("Usage: Rscript plotter.R -i <input_file> -p <output_prefix>")
}

input_index <- which(args == "-i")
prefix_index <- which(args == "-p")

# Extract input file path and output prefix
input_file <- args[input_index + 1]
prefix <- args[prefix_index + 1]

# Read input table
data <- read.csv(input_file, header = TRUE)

# Reorder chromosomes if "Chromosome" column exists
if ("Chromosome" %in% colnames(data)) {
  chromosome_order <- c(paste0("chr", 1:23), "chrX", "chrY", "chrM")
  data$Chromosome <- factor(data$Chromosome, levels = chromosome_order)
} else {
  stop("Input data does not contain a 'Chromosome' column.")
}

# Create bar plots for every two columns except the first one
for (i in seq(2, ncol(data), by = 2)) {
  # Extract relevant columns for each plot
  plot_data <- data[, c(1, i, i + 1)]

  # Reshape data for plotting
  plot_data_long <- melt(plot_data, id.vars = "Chromosome")

  # Set factor levels for the 'variable' variable
  plot_data_long$variable <- factor(plot_data_long$variable, levels = unique(plot_data_long$variable))

  # Rename columns based on column names
  col_names <- names(data)[i]
  if (grepl("Mismatch", col_names)) {
    plot_title <- paste(prefix, ": Mismatch rate comparison")
    y_axis_title <- "mismatch"
  } else if (grepl("Soft", col_names)) {
    plot_title <- paste(prefix, ": Soft clipping comparison")
    y_axis_title <- "n"
  } else if (grepl("Unmapped", col_names)) {
    plot_title <- paste(prefix, ": Unmapped reads mapped in other assembly")
    y_axis_title <- "counts"
  } else {
    plot_title <- paste(prefix, ": Multi-mapping rates comparison")
    y_axis_title <- "multimap"
  }

  # Create bar plot
  plot <- ggplot(plot_data_long, aes(x = Chromosome, y = value, fill = variable)) +
    geom_bar(stat = "identity", position = position_dodge2(width = 0.8), color = "black") + # Add black outlines
    labs(title = plot_title,
         x = "Chromosome",
         y =  y_axis_title) +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1),
          panel.grid.major = element_blank(), # Remove major grid lines
          panel.grid.minor = element_blank(), # Remove minor grid lines
          plot.title = element_text(hjust = 0.5)) + # Center title
    scale_fill_manual(values = c("#00AFBB", "#E7B800"), # Use specified colors
                      name = "Assembly Type",
                      labels = c("non-T2T", "T2T")) +
    guides(fill = guide_legend(title = "Assembly Type"))

  # Save the plot with specified prefix and .png extension, adjusting width and height
  ggsave(paste0(prefix, "_", names(data)[i], "_", names(data)[i + 1], ".png"),
         plot,
         bg = "white",
         width = 10, # Adjust width of the saved PNG file
         height = 6) # Adjust height of the saved PNG file
}

