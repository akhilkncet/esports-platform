// API Configuration
// Using relative URL since frontend and backend are on the same server
const API_BASE_URL = '/api';

// CSRF Token management
let csrfToken = null;

async function getCSRFToken() {
    if (!csrfToken) {
        try {
            const response = await fetch('/api/get-csrf-token/', {
                credentials: 'include'
            });
            const data = await response.json();
            csrfToken = data.csrfToken;
        } catch (error) {
            console.error('Error getting CSRF token:', error);
        }
    }
    return csrfToken;
}

// Authentication functions
async function checkAuthentication() {
    try {
        const response = await fetch('/api/check-auth/', {
            credentials: 'include'
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.authenticated) {
                // Update username display
                const usernameDisplay = document.getElementById('usernameDisplay');
                if (usernameDisplay) {
                    usernameDisplay.textContent = `👤 ${data.username}`;
                }
                // Store user data
                localStorage.setItem('isAuthenticated', 'true');
                localStorage.setItem('username', data.username);
                localStorage.setItem('userId', data.user_id);
                return true;
            }
        }
        
        // Not authenticated, but don't redirect - let Django handle it
        return false;
    } catch (error) {
        console.error('Authentication check failed:', error);
        return false;
    }
}

async function handleLogout() {
    try {
        const token = await getCSRFToken();
        const response = await fetch('/api/logout/', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'X-CSRFToken': token
            }
        });
        
        if (response.ok) {
            // Clear local storage
            localStorage.removeItem('isAuthenticated');
            localStorage.removeItem('username');
            localStorage.removeItem('userId');
            
            // Redirect to login
            window.location.href = '/login/';
        }
    } catch (error) {
        console.error('Logout error:', error);
        // Force redirect anyway
        localStorage.clear();
        window.location.href = '/login/';
    }
}

// API Client
const api = {
    // Helper method for making requests
    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        
        // Get CSRF token for non-GET requests
        if (options.method && options.method !== 'GET') {
            const token = await getCSRFToken();
            options.headers = {
                ...options.headers,
                'X-CSRFToken': token
            };
        }
        
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            credentials: 'include',
            ...options,
        };

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || errorData.message || `HTTP error! status: ${response.status}`);
            }
            
            // Handle 204 No Content responses
            if (response.status === 204) {
                return null;
            }
            
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    },

    // Teams API
    async getTeams() {
        return await this.request('/teams/teams/');
    },

    async getTeam(id) {
        return await this.request(`/teams/teams/${id}/`);
    },

    async createTeam(teamData) {
        return await this.request('/teams/teams/', {
            method: 'POST',
            body: JSON.stringify(teamData),
        });
    },

    async updateTeam(id, teamData) {
        return await this.request(`/teams/teams/${id}/`, {
            method: 'PUT',
            body: JSON.stringify(teamData),
        });
    },

    async deleteTeam(id) {
        return await this.request(`/teams/teams/${id}/`, {
            method: 'DELETE',
        });
    },

    // Tournaments API
    async getTournaments() {
        return await this.request('/tournaments/tournaments/');
    },

    async getTournament(id) {
        return await this.request(`/tournaments/tournaments/${id}/`);
    },

    async createTournament(tournamentData) {
        return await this.request('/tournaments/tournaments/', {
            method: 'POST',
            body: JSON.stringify(tournamentData),
        });
    },

    async updateTournament(id, tournamentData) {
        return await this.request(`/tournaments/tournaments/${id}/`, {
            method: 'PUT',
            body: JSON.stringify(tournamentData),
        });
    },

    async deleteTournament(id) {
        return await this.request(`/tournaments/tournaments/${id}/`, {
            method: 'DELETE',
        });
    },

    // Groups API
    async getGroups(tournamentId = null) {
        const endpoint = tournamentId 
            ? `/tournaments/groups/?tournament=${tournamentId}`
            : '/tournaments/groups/';
        return await this.request(endpoint);
    },

    async getGroup(id) {
        return await this.request(`/tournaments/groups/${id}/`);
    },

    async createGroup(groupData) {
        return await this.request('/tournaments/groups/', {
            method: 'POST',
            body: JSON.stringify(groupData),
        });
    },

    async updateGroup(id, groupData) {
        return await this.request(`/tournaments/groups/${id}/`, {
            method: 'PUT',
            body: JSON.stringify(groupData),
        });
    },

    async deleteGroup(id) {
        return await this.request(`/tournaments/groups/${id}/`, {
            method: 'DELETE',
        });
    },

    // Matches API
    async getMatches(groupId = null) {
        const endpoint = groupId 
            ? `/tournaments/matches/?group=${groupId}`
            : '/tournaments/matches/';
        return await this.request(endpoint);
    },

    async getMatch(id) {
        return await this.request(`/tournaments/matches/${id}/`);
    },

    async createMatch(matchData) {
        return await this.request('/tournaments/matches/', {
            method: 'POST',
            body: JSON.stringify(matchData),
        });
    },

    async updateMatch(id, matchData) {
        return await this.request(`/tournaments/matches/${id}/`, {
            method: 'PUT',
            body: JSON.stringify(matchData),
        });
    },

    async deleteMatch(id) {
        return await this.request(`/tournaments/matches/${id}/`, {
            method: 'DELETE',
        });
    },

    // Standings API
    async getStandings(tournamentId = null) {
        const endpoint = tournamentId 
            ? `/tournaments/standings/?tournament=${tournamentId}`
            : '/tournaments/standings/';
        return await this.request(endpoint);
    },

    async getStanding(id) {
        return await this.request(`/tournaments/standings/${id}/`);
    },

    // Final Stages API
    async getFinalStages(tournamentId = null) {
        const endpoint = tournamentId 
            ? `/tournaments/final-stages/?tournament=${tournamentId}`
            : '/tournaments/final-stages/';
        return await this.request(endpoint);
    },

    async getFinalStage(id) {
        return await this.request(`/tournaments/final-stages/${id}/`);
    },

    // Final Matches API
    async getFinalMatches(finalStageId = null) {
        const endpoint = finalStageId 
            ? `/tournaments/final-matches/?final_stage=${finalStageId}`
            : '/tournaments/final-matches/';
        return await this.request(endpoint);
    },

    async getFinalMatch(id) {
        return await this.request(`/tournaments/final-matches/${id}/`);
    },

    // Users API
    async getUsers() {
        return await this.request('/accounts/users/');
    },

    async getUser(id) {
        return await this.request(`/accounts/users/${id}/`);
    },
};

// Utility Functions

// Escape HTML to prevent XSS
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Format date
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Format number with commas
function formatNumber(num) {
    if (!num) return '0';
    return parseFloat(num).toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

// Format status text
function formatStatus(status) {
    if (!status) return 'Unknown';
    return status
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

// Close modal
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    }
}

// Close modal when clicking outside
window.addEventListener('click', (event) => {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
});

// Close modal on Escape key
document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            if (modal.style.display === 'flex') {
                modal.style.display = 'none';
            }
        });
    }
});

// Show notification
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notif => notif.remove());

    // Create new notification
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);

    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add slideout animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
`;
document.head.appendChild(style);

// Handle API errors globally
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    
    // Check if it's a network error
    if (event.reason instanceof TypeError && event.reason.message.includes('fetch')) {
        showNotification('Cannot connect to the server. Please make sure the backend is running on http://localhost:8000', 'error');
    }
});

// Log API base URL on load
console.log('Esports Platform Frontend');
console.log('API Base URL:', API_BASE_URL);
console.log('Make sure the Django backend is running on http://localhost:8000');
