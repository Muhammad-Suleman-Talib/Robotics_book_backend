---
sidebar_position: 10
title: Internationalization (i18n) Guide
---

# Internationalization (i18n) Guide

This guide outlines the process for setting up and managing multilingual content using Docusaurus's internationalization (i18n) features. The site currently supports English (en), Urdu (ur), and French (fr).

## 1. Docusaurus i18n Configuration

The core i18n configuration is located in `docusaurus.config.ts` within the `book-site/` directory.

```typescript
// docusaurus.config.ts
i18n: {
  defaultLocale: 'en',
  locales: ['en', 'ur', 'fr'],
  localeConfigs: {
    en: {
      label: 'English',
      direction: 'ltr',
      htmlLang: 'en-US',
    },
    ur: {
      label: 'اردو',
      direction: 'rtl',
      htmlLang: 'ur-PK',
    },
    fr: {
      label: 'Français',
      direction: 'ltr',
      htmlLang: 'fr-FR',
    },
  },
},
```

-   `defaultLocale`: Sets the default language for your site (e.g., 'en').
-   `locales`: An array of all supported locales.
-   `localeConfigs`: Provides specific configurations for each locale, including:
    -   `label`: The display name for the language in the language switcher.
    -   `direction`: Text direction (`ltr` for left-to-right, `rtl` for right-to-left). This is crucial for languages like Urdu.
    -   `htmlLang`: The `lang` attribute for the `<html>` tag, important for SEO and accessibility.

## 2. Directory Structure for Translations

Docusaurus organizes translated content within the `i18n/` directory in your `book-site/` root. Each locale gets its own subdirectory.

```
book-site/
├── i18n/
│   ├── en/
│   ├── ur/
│   │   └── docusaurus-plugin-content-docs/
│   │       └── current/
│   │           └── intro.md # Urdu translation for docs/intro.md
│   └── fr/
│       └── docusaurus-plugin-content-docs/
│           └── current/
│               └── intro.md # French translation for docs/intro.md
├── docs/
│   └── intro.md # Original English content
└── ...
```

-   For document translations (like `docs/intro.md`), the structure mirrors the original `docs/` folder within `i18n/<locale>/docusaurus-plugin-content-docs/current/`.

## 3. Translating Content

### Documents (Markdown files)

To translate a Markdown document (e.g., `docs/intro.md`):

1.  Create the corresponding directory structure under `book-site/i18n/<locale>/docusaurus-plugin-content-docs/current/`.
    -   Example for Urdu `intro.md`: `book-site/i18n/ur/docusaurus-plugin-content-docs/current/intro.md`
    -   Example for French `intro.md`: `book-site/i18n/fr/docusaurus-plugin-content-docs/current/intro.md`
2.  Copy the original Markdown content into the new locale-specific file.
3.  Translate the content within the new file. Ensure the front matter (`title`, `sidebar_position`, etc.) is also translated or adapted as needed.

Example of `intro.md` in Urdu (`book-site/i18n/ur/docusaurus-plugin-content-docs/current/intro.md`):

```markdown
---
title: تعارف
---

ہیلو ورلڈ! یہ تعارفی باب کا اردو ترجمہ ہے۔

یہ ڈوکوسورس میں بین الاقوامی کاری کی جانچ کے لیے ہے۔
```

### Static Text (UI elements, etc.)

For translating UI elements (e.g., Navbar labels, footer text), Docusaurus uses JSON files. These are typically located under `book-site/i18n/<locale>/docusaurus-theme-classic/` (or similar plugin-specific directories).

1.  To generate base translation files, run:
    ```bash
    cd book-site
    npm run write-translations
    ```
    This command will extract translatable strings and create `.json` files in the `i18n/<locale>/` directories.
2.  Edit the generated `.json` files to provide the translations.

## 4. Building and Serving

After making translation changes, you need to rebuild the Docusaurus site:

```bash
cd book-site
npm install # if dependencies changed
npm run build
```

To serve the built site locally for testing:

```bash
cd book-site
npm run serve
```

Then, access `http://localhost:3000` (or the indicated URL) in your browser and use the language switcher to test the translations.

## 5. RTL (Right-to-Left) Support

For languages like Urdu, `direction: 'rtl'` is set in `docusaurus.config.ts`. Docusaurus themes typically include built-in RTL support for common components. If you have custom CSS, you might need to provide RTL-specific styles. For example, by creating `custom.css` and `custom.rtl.css` in `book-site/src/css/`.
