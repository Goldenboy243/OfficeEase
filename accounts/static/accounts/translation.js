class Translator {
    constructor() {
        this.currentLang = localStorage.getItem('selectedLanguage') || 'en';
        this.translations = {};
        this.loadTranslations();
    }

    async loadTranslations() {
        try {
            const response = await fetch('/static/accounts/translations.json');
            this.translations = await response.json();
            this.applyTranslations();
        } catch (error) {
            console.error('Failed to load translations:', error);
        }
    }

    setLanguage(lang) {
        this.currentLang = lang;
        localStorage.setItem('selectedLanguage', lang);
        this.applyTranslations();
        this.updateLanguageSelector();
    }

    applyTranslations() {
        if (!this.translations[this.currentLang]) return;

        // Update all elements with data-translate attribute
        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            const translation = this.getTranslation(key);

            if (translation) {
                if (element.tagName === 'INPUT' && element.hasAttribute('placeholder')) {
                    element.placeholder = translation;
                } else if (element.tagName === 'TITLE') {
                    document.title = translation;
                } else {
                    element.innerHTML = translation;
                }
            }
        });

        // Update HTML lang attribute
        document.documentElement.lang = this.currentLang;

        // Update language selector display
        this.updateLanguageSelector();
    }

    getTranslation(key) {
        const keys = key.split('.');
        let value = this.translations[this.currentLang];

        for (const k of keys) {
            if (value && typeof value === 'object') {
                value = value[k];
            } else {
                return null;
            }
        }

        return value || key;
    }

    updateLanguageSelector() {
        // Update the language display in the dropdown
        const langDisplay = document.querySelector('.language-selector .current-lang');
        if (langDisplay) {
            langDisplay.textContent = this.currentLang.toUpperCase();
        }

        // Update active state in dropdown
        document.querySelectorAll('.language-option').forEach(option => {
            option.classList.remove('active');
            if (option.getAttribute('data-lang') === this.currentLang) {
                option.classList.add('active');
            }
        });
    }

    // Method to get current language
    getCurrentLanguage() {
        return this.currentLang;
    }
}

// Initialize translator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.translator = new Translator();

    // Set up language selector event listeners
    document.querySelectorAll('.language-option').forEach(option => {
        option.addEventListener('click', (e) => {
            e.preventDefault();
            const lang = option.getAttribute('data-lang');
            window.translator.setLanguage(lang);
        });
    });
});
