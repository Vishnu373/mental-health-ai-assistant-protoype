const templateCache = new Map();

export async function loadTemplate(templateName) {
    // Check cache first
    if (templateCache.has(templateName)) {
        return templateCache.get(templateName);
    }
    
    try {
        const response = await fetch(`/src/templates/${templateName}.html`);
        if (!response.ok) {
            throw new Error(`Template not found: ${templateName}`);
        }
        
        const template = await response.text();
        templateCache.set(templateName, template);
        return template;
        
    } catch (error) {
        console.error(`Error loading template ${templateName}:`, error);
        throw error;
    }
}

export function renderTemplate(template, data = {}) {
    let rendered = template;
    
    // Replace {{key}} placeholders with values
    for (const [key, value] of Object.entries(data)) {
        const placeholder = new RegExp(`{{${key}}}`, 'g');
        rendered = rendered.replace(placeholder, value || '');
    }
    
    return rendered;
}