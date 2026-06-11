<div align="center">
  <h1 align="center">Rule Taxonomy and Evolution in AI IDEs: A Mining and Survey Study</h1>
</div>

<div align="center">
    <a href="https://github.com/breezesway/Rules_in_AI_IDEs">
        <img src="https://img.shields.io/badge/GitHub-000?logo=github&logoColor=FFE165&style=for-the-badge" alt="">
    </a>
    <a href="https://arxiv.org/abs/2606.12231">
        <img src="https://img.shields.io/badge/Paper-000?logoColor=FFE165&logo=arxiv&style=for-the-badge" alt="">
    </a>
    <hr>
</div>

## ✨ Repository Overview

This repository is the online replication package for the paper **Rule Taxonomy and Evolution in AI IDEs: A Mining and Survey Study**. It contains the raw data, analysis scripts, intermediate results, and chart-generation code used throughout the study.

## 📋 Directory Structure

### `data_collection/`

Scripts and outputs for collecting GitHub project data.

- **`cursor/`**, **`kiro/`**, **`qoder/`**, **`trae/`**, **`windsurf/`**: Search and filtering scripts for GitHub repositories associated with five AI IDEs—Cursor, Kiro, Qoder, Trae, and Windsurf.
- **`projects_info.csv`**: Summary of the projects ultimately selected for the study.

### `rq1_rules/`

Data and charts for RQ1 (rule taxonomy and survey).

- **`rules/`**: A total of 7,310 rules stored in JSON format, along with the original rule files from each project.
- **`rq1_result_charts/`**: Scripts for generating RQ1 result charts, plus the generated chart files.

### `rq2_1_evolved_rules/`

Data and charts for RQ2.1 (rule evolution).

- **`file_diffs/`**: Change records (diff files) for all evolved rules.
- **`rq2_1_result_charts/`**: Scripts for generating RQ2.1 result charts, plus the generated chart files.

### `rq2_2_rule_reasons/`

Data, analysis, and charts for RQ2.2 (reasons for rule changes).

- **CSV, JSON files, and Python scripts** at the root level: Sampled data for manual verification and related analysis code.
- **`LLM_filter/`**: Scripts and results for filtering rule-change reasons using LLMs.
- **`rq2_2_result_charts/`**: Scripts for generating RQ2.2 result charts, plus the generated chart files.

### `rq2_3_rule_compilance/`

Data and analysis for RQ2.3 (rule compliance).

- **`LLM_filter/`**: Sampled data and code for manual verification, along with scripts and results for LLM-based filtering.

### `survey/`

Scripts, data, and charts for the online survey study.

- **`collect_email/`**: Scripts for collecting contributor email addresses from GitHub.
- **`email/`**: Scripts for sending survey invitation emails.
- **`survey_results/`**: The final collected survey responses—99 responses in English and Chinese.
- **`education_professional_duration/`**, **`role_domain_ide/`**: Scripts for generating survey-related charts.

## 🚀 GitHub Project Snapshots

Due to their large size, snapshots of the selected GitHub project repositories are not included directly in this repository. They are hosted on Zenodo instead:

- **DOI**: [10.5281/zenodo.20348574](https://doi.org/10.5281/zenodo.20348574)

Please download the complete project snapshot archive via the link above.

## 🙂 Contact

If you have any questions, please contact: [caigz1999@foxmail.com](mailto:caigz1999@foxmail.com)

## 📝 Citation

```bibtex
@article{Ca2026Rules,
  author = {Cai, Guangzong and Li, Ruiyin and Liang, Peng and Li, Zengyang and Shahin, Mojtaba},
  title = {{Rule Taxonomy and Evolution in AI IDEs: A Mining and Survey Study}},
  journal={arXiv preprint arXiv:2606.12231},
  year={2026}
}
```
