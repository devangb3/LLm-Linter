/**
 * Utility functions for the sample application.
 *
 * This file contains various utility functions that are used across
 * the frontend and backend. Some functions have repeated logic.
 */

// Date formatting utilities (repeated in multiple places)
function formatDate(date) {
    return date.toISOString().split('T')[0];
}

function formatDateTime(date) {
    return date.toISOString();
}

function getRelativeTime(date) {
    const now = new Date();
    const diff = now - date;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes} minutes ago`;
    if (hours < 24) return `${hours} hours ago`;
    return `${days} days ago`;
}

// Validation utilities (scattered across files)
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validateUsername(username) {
    return username && username.length >= 3 && username.length <= 20;
}

function validatePassword(password) {
    return password && password.length >= 8;
}

// API call utilities (repeated patterns)
async function apiCall(endpoint, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const finalOptions = { ...defaultOptions, ...options };

    try {
        const response = await fetch(endpoint, finalOptions);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Authentication utilities (duplicated auth logic)
function getAuthToken() {
    return localStorage.getItem('auth_token');
}

function setAuthToken(token) {
    localStorage.setItem('auth_token', token);
}

function removeAuthToken() {
    localStorage.removeItem('auth_token');
}

function isAuthenticated() {
    const token = getAuthToken();
    if (!token) return false;

    // This is a simple check - real apps should validate token expiration
    return true;
}

// DOM manipulation utilities (mixed with business logic)
function showError(message) {
    const errorDiv = document.getElementById('error-message');
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 5000);
    }
}

function showSuccess(message) {
    const successDiv = document.getElementById('success-message');
    if (successDiv) {
        successDiv.textContent = message;
        successDiv.style.display = 'block';
        setTimeout(() => {
            successDiv.style.display = 'none';
        }, 3000);
    }
}

// Form handling utilities
function serializeForm(form) {
    const data = new FormData(form);
    const result = {};
    for (let [key, value] of data.entries()) {
        result[key] = value;
    }
    return result;
}

function clearForm(form) {
    form.reset();
}

// Export for module usage (inconsistent export pattern)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        formatDate,
        formatDateTime,
        getRelativeTime,
        validateEmail,
        validateUsername,
        validatePassword,
        apiCall,
        getAuthToken,
        setAuthToken,
        removeAuthToken,
        isAuthenticated,
        showError,
        showSuccess,
        serializeForm,
        clearForm
    };
}
