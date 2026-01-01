PDF_CSS = """
<style>
    @page {
        size: A4;
        margin: 2cm 2.5cm 3cm 2.5cm;

        @top-center {
            content: "YouTube Video Analysis";
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 10px;
            color: #666;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
        }

        @bottom-right {
            content: "Page " counter(page) " of " counter(pages);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 10px;
            color: #666;
        }
    }

    * {
        box-sizing: border-box;
    }

    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        color: #333;
        margin: 0;
        padding: 0;
        font-size: 11pt;
    }

    .document-header {
        text-align: center;
        border-bottom: 3px solid #007acc;
        padding-bottom: 20px;
        margin-bottom: 40px;
        page-break-after: avoid;
    }

    .document-title {
        font-size: 24pt;
        font-weight: bold;
        color: #007acc;
        margin: 0 0 10px 0;
        line-height: 1.2;
    }

    .document-meta {
        font-size: 10pt;
        color: #666;
        margin: 0;
    }

    .section {
        margin-bottom: 25px;
        page-break-inside: avoid;
    }

    .section h1 {
        font-size: 18pt;
        color: #007acc;
        border-left: 4px solid #007acc;
        padding-left: 15px;
        margin: 25px 0 15px 0;
        page-break-after: avoid;
    }

    .section h2 {
        font-size: 14pt;
        color: #333;
        margin: 20px 0 10px 0;
        page-break-after: avoid;
    }

    .section h3 {
        font-size: 12pt;
        color: #555;
        margin: 15px 0 8px 0;
        page-break-after: avoid;
    }

    .executive-summary {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin-bottom: 25px;
        page-break-inside: avoid;
    }

    .executive-summary h2 {
        color: #28a745;
        margin-top: 0;
    }

    .key-points {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        margin-bottom: 20px;
    }

    ul, ol {
        padding-left: 20px;
        margin: 10px 0;
    }

    li {
        margin-bottom: 6px;
        line-height: 1.5;
    }

    .quote {
        font-style: italic;
        background-color: #f8f9fa;
        padding: 15px;
        border-left: 4px solid #6c757d;
        margin: 15px 0;
        page-break-inside: avoid;
    }

    .resources {
        background-color: #e7f3ff;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #007acc;
        margin: 15px 0;
    }

    .step-guide {
        background-color: #f0f8f0;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin: 15px 0;
        page-break-inside: avoid;
    }

    .step-guide ol {
        margin: 10px 0 0 0;
    }

    .step-guide li {
        margin-bottom: 8px;
        font-weight: 500;
    }

    p {
        margin: 10px 0;
        text-align: justify;
    }

    .page-break {
        page-break-before: always;
    }

    .no-break {
        page-break-inside: avoid;
    }

    .footer-note {
        font-size: 9pt;
        color: #666;
        text-align: center;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #ddd;
    }

    /* Table styling for structured content */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
    }

    th, td {
        padding: 8px 12px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }

    th {
        background-color: #f8f9fa;
        font-weight: bold;
        color: #333;
    }

    /* Responsive adjustments */
    @media print {
        .section {
            page-break-inside: avoid;
        }
    }
</style>
"""
