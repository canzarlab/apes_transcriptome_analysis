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

# Identify the columns related to the comparison of reads that were unmapped before and are mapped now
unmapped_columns <- grep("Unmapped", names(data))

# Plot only the data related to non-T2T for the unmapped columns
for (col_index in unmapped_columns) {
  # Extract relevant columns for each plot
  plot_data <- data[, c(1, col_index)]

  # Reshape data for plotting
  plot_data_long <- melt(plot_data, id.vars = "Chromosome")

  # Rename columns based on column names
  col_names <- names(data)[col_index]
  plot_title <- paste(prefix, ": Unmapped reads mapped in other assembly")
  y_axis_title <- "counts"

  # Create bar plot
  plot <- ggplot(plot_data_long, aes(x = Chromosome, y = value)) +
    geom_bar(stat = "identity", position = position_dodge2(width = 0.8), color = "black", fill = "#00AFBB") + # Add black outlines
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
  ggsave(paste0(prefix, "_", names(data)[col_index], ".png"),
         plot,
         bg = "white",
         width = 10, # Adjust width of the saved PNG file
         height = 6) # Adjust height of the saved PNG file
}

