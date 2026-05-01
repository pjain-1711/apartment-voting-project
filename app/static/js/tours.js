// =====================================================
// IN-APP TOUR SYSTEM - First Time User Onboarding
// =====================================================

// Check if user has seen a specific tour
function hasSeenTour(tourName) {
    return localStorage.getItem(`tour_${tourName}_completed`) === 'true';
}

// Mark tour as completed
function markTourCompleted(tourName) {
    localStorage.setItem(`tour_${tourName}_completed`, 'true');
}

// Reset all tours (for testing)
function resetAllTours() {
    const keys = Object.keys(localStorage);
    keys.forEach(key => {
        if (key.startsWith('tour_')) {
            localStorage.removeItem(key);
        }
    });
}

// Common tour buttons
const tourButtons = {
    next: {
        text: 'Next',
        action: function() { this.next(); }
    },
    back: {
        text: 'Back',
        action: function() { this.back(); }
    },
    skip: {
        text: 'Skip Tour',
        classes: 'shepherd-button-secondary',
        action: function() { this.cancel(); }
    },
    done: {
        text: 'Got it!',
        action: function() { this.complete(); }
    }
};

// =====================================================
// LANDING PAGE TOUR
// =====================================================
function startLandingTour() {
    if (hasSeenTour('landing')) return;

    const tour = new Shepherd.Tour({
        useModalOverlay: true,
        defaultStepOptions: {
            classes: 'shepherd-theme-custom',
            scrollTo: true,
            cancelIcon: {
                enabled: true
            }
        }
    });

    tour.addStep({
        id: 'welcome',
        text: '<h3>Welcome to the Voting System!</h3><p>This is the Wing Representative Election system for Assetz Sun and Sanctum. Let me show you around.</p>',
        buttons: [tourButtons.skip, tourButtons.next]
    });

    tour.addStep({
        id: 'vote-button',
        text: '<p>Click here to start the voting process. You\'ll need your flat number to vote.</p>',
        attachTo: {
            element: 'a[href*="vote"]',
            on: 'bottom'
        },
        buttons: [tourButtons.back, tourButtons.skip, tourButtons.next]
    });

    tour.addStep({
        id: 'admin-section',
        text: '<p>Administrators can access the admin panel to manage nominations, view progress, and declare results.</p>',
        attachTo: {
            element: 'a[href*="admin"]',
            on: 'bottom'
        },
        buttons: [tourButtons.back, tourButtons.skip, tourButtons.done]
    });

    tour.on('complete', () => markTourCompleted('landing'));
    tour.on('cancel', () => markTourCompleted('landing'));

    tour.start();
}

// =====================================================
// VOTER INFO PAGE TOUR
// =====================================================
function startVoterInfoTour() {
    if (hasSeenTour('voter_info')) return;

    const tour = new Shepherd.Tour({
        useModalOverlay: true,
        defaultStepOptions: {
            classes: 'shepherd-theme-custom',
            scrollTo: true,
            cancelIcon: {
                enabled: true
            }
        }
    });

    tour.addStep({
        id: 'welcome-voting',
        text: '<h3>Ready to Vote?</h3><p>Fill in your details to begin the voting process. Make sure you have your flat number ready.</p>',
        buttons: [tourButtons.skip, tourButtons.next]
    });

    tour.addStep({
        id: 'voter-name',
        text: '<p>Enter your full name as it should appear in the records.</p>',
        attachTo: {
            element: '#voter_name',
            on: 'bottom'
        },
        buttons: [tourButtons.back, tourButtons.skip, tourButtons.next]
    });

    tour.addStep({
        id: 'flat-number',
        text: '<p>Enter your 4-digit flat number. The first digit indicates your wing (e.g., 1065 is in Wing 1).</p>',
        attachTo: {
            element: '#flat_number',
            on: 'bottom'
        },
        buttons: [tourButtons.back, tourButtons.skip, tourButtons.next]
    });

    tour.addStep({
        id: 'important-notes',
        text: '<p><strong>Important:</strong> Each flat can only vote once. You\'ll have 2 minutes to complete your vote after submitting this form.</p>',
        buttons: [tourButtons.back, tourButtons.skip, tourButtons.done]
    });

    tour.on('complete', () => markTourCompleted('voter_info'));
    tour.on('cancel', () => markTourCompleted('voter_info'));

    tour.start();
}

// =====================================================
// VOTE SELECTION PAGE TOUR
// =====================================================
function startVoteSelectionTour() {
    if (hasSeenTour('vote_selection')) return;

    const tour = new Shepherd.Tour({
        useModalOverlay: true,
        defaultStepOptions: {
            classes: 'shepherd-theme-custom',
            scrollTo: true,
            cancelIcon: {
                enabled: true
            }
        }
    });

    tour.addStep({
        id: 'timer-warning',
        text: '<h3>Time Limit Active!</h3><p>You have 2 minutes to make your selections. The timer at the top shows your remaining time.</p>',
        attachTo: {
            element: '#timerAlert',
            on: 'bottom'
        },
        buttons: [tourButtons.skip, tourButtons.next]
    });

    tour.addStep({
        id: 'male-nominees',
        text: '<p>Select up to 2 male representatives by clicking on the cards. You must select at least one.</p>',
        attachTo: {
            element: '.mb-5',
            on: 'bottom'
        },
        buttons: [tourButtons.back, tourButtons.skip, tourButtons.next]
    });

    tour.addStep({
        id: 'female-nominees',
        text: '<p>Select up to 2 female representatives. Click the cards to select or deselect nominees.</p>',
        attachTo: {
            element: '.mb-4',
            on: 'bottom'
        },
        buttons: [tourButtons.back, tourButtons.skip, tourButtons.next]
    });

    tour.addStep({
        id: 'submit-vote',
        text: '<p>Once you\'ve made your selections, click "Review & Confirm" to proceed. You\'ll have a chance to review before final submission.</p>',
        buttons: [tourButtons.back, tourButtons.skip, tourButtons.done]
    });

    tour.on('complete', () => markTourCompleted('vote_selection'));
    tour.on('cancel', () => markTourCompleted('vote_selection'));

    tour.start();
}

// =====================================================
// CONFIRMATION PAGE TOUR
// =====================================================
function startConfirmationTour() {
    if (hasSeenTour('confirmation')) return;

    const tour = new Shepherd.Tour({
        useModalOverlay: true,
        defaultStepOptions: {
            classes: 'shepherd-theme-custom',
            scrollTo: true,
            cancelIcon: {
                enabled: true
            }
        }
    });

    tour.addStep({
        id: 'review',
        text: '<h3>Review Your Selections</h3><p>Please carefully review your choices. Once you submit, you cannot change your vote.</p>',
        buttons: [tourButtons.skip, tourButtons.next]
    });

    tour.addStep({
        id: 'voter-details',
        text: '<p>Verify that your name and flat number are correct.</p>',
        attachTo: {
            element: '.list-unstyled',
            on: 'bottom'
        },
        buttons: [tourButtons.back, tourButtons.skip, tourButtons.next]
    });

    tour.addStep({
        id: 'final-submit',
        text: '<p>If everything looks correct, click "Submit Vote" to finalize. If you need to change your selections, click "Cancel" to go back.</p>',
        buttons: [tourButtons.back, tourButtons.skip, tourButtons.done]
    });

    tour.on('complete', () => markTourCompleted('confirmation'));
    tour.on('cancel', () => markTourCompleted('confirmation'));

    tour.start();
}

// =====================================================
// ADMIN DASHBOARD TOUR
// =====================================================
function startAdminDashboardTour() {
    if (hasSeenTour('admin_dashboard')) return;

    const tour = new Shepherd.Tour({
        useModalOverlay: true,
        defaultStepOptions: {
            classes: 'shepherd-theme-custom',
            scrollTo: true,
            cancelIcon: {
                enabled: true
            }
        }
    });

    tour.addStep({
        id: 'admin-welcome',
        text: '<h3>Admin Dashboard</h3><p>Welcome to the admin panel. From here you can manage all aspects of the election.</p>',
        buttons: [tourButtons.skip, tourButtons.next]
    });

    tour.addStep({
        id: 'sidebar',
        text: '<p>Use this sidebar to navigate between different admin sections: Wings, Nominees, Progress, Settings, etc.</p>',
        attachTo: {
            element: '.admin-sidebar',
            on: 'right'
        },
        buttons: [tourButtons.back, tourButtons.skip, tourButtons.next]
    });

    tour.addStep({
        id: 'stats',
        text: '<p>View key statistics about the election at a glance: total wings, nominees, votes cast, and participation rate.</p>',
        buttons: [tourButtons.back, tourButtons.skip, tourButtons.next]
    });

    tour.addStep({
        id: 'settings-control',
        text: '<p>Use the Settings page to enable/disable voting and control when results are visible to the public.</p>',
        buttons: [tourButtons.back, tourButtons.skip, tourButtons.done]
    });

    tour.on('complete', () => markTourCompleted('admin_dashboard'));
    tour.on('cancel', () => markTourCompleted('admin_dashboard'));

    tour.start();
}

// =====================================================
// RESULTS PAGE TOUR
// =====================================================
function startResultsTour() {
    if (hasSeenTour('results')) return;

    const tour = new Shepherd.Tour({
        useModalOverlay: true,
        defaultStepOptions: {
            classes: 'shepherd-theme-custom',
            scrollTo: true,
            cancelIcon: {
                enabled: true
            }
        }
    });

    tour.addStep({
        id: 'results-welcome',
        text: '<h3>Election Results</h3><p>View the complete results of the Wing Representative Elections.</p>',
        buttons: [tourButtons.skip, tourButtons.next]
    });

    tour.addStep({
        id: 'pdf-download',
        text: '<p>Download a PDF copy of the results for your records or to share with others.</p>',
        attachTo: {
            element: '.btn-danger',
            on: 'bottom'
        },
        buttons: [tourButtons.back, tourButtons.skip, tourButtons.next]
    });

    tour.addStep({
        id: 'wing-results',
        text: '<p>Results are organized by wing. Winners are highlighted with a badge. Each candidate\'s vote count and rank are displayed.</p>',
        buttons: [tourButtons.back, tourButtons.skip, tourButtons.done]
    });

    tour.on('complete', () => markTourCompleted('results'));
    tour.on('cancel', () => markTourCompleted('results'));

    tour.start();
}

// =====================================================
// UTILITY: Manual tour trigger (for "Show Tour" button)
// =====================================================
function showTourManually(tourName) {
    // Temporarily clear the tour completion flag
    localStorage.removeItem(`tour_${tourName}_completed`);

    // Start the appropriate tour
    switch(tourName) {
        case 'landing':
            startLandingTour();
            break;
        case 'voter_info':
            startVoterInfoTour();
            break;
        case 'vote_selection':
            startVoteSelectionTour();
            break;
        case 'confirmation':
            startConfirmationTour();
            break;
        case 'admin_dashboard':
            startAdminDashboardTour();
            break;
        case 'results':
            startResultsTour();
            break;
    }
}
