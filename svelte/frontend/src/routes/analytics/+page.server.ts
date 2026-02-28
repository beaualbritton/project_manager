// src/routes/analytics/+page.server.ts
import type { PageServerLoad } from './$types';

// Define the shape internally (or move to $lib/types.ts)
interface InsightCategory {
    category: 'Budget Risk' | 'Scheduling' | 'Team Performance';
    headline: string;
    detail: string;
    severity: 'low' | 'medium' | 'high';
    isAllClear: boolean;
}

export const load: PageServerLoad = async () => {
    const aiInsights: InsightCategory[] = [
        {
            category: 'Budget Risk',
            headline: 'Frontend Core is approaching budget limits',
            detail: 'The Design System Overhaul has burned 75% of its $5,000 budget while only being 50% complete. You may need to request a $1,500 overage approval by Friday.',
            severity: 'medium',
            isAllClear: false
        },
        {
            category: 'Scheduling',
            headline: 'Critical blocker on User Authentication UI',
            detail: 'This task is currently 3 days past its deadline. Because it is a dependency for the Dashboard Analytics View, the entire sprint timeline is now at risk of slipping.',
            severity: 'high',
            isAllClear: false
        },
        {
            category: 'Team Performance',
            headline: 'Capacity is balanced and healthy',
            detail: 'No team members are currently overallocated. Sarah and Marcus are maintaining a steady velocity with no flagged blockers in their recent activity.',
            severity: 'low',
            isAllClear: true 
        }
    ];

    // SvelteKit automatically infers the type of this return object
    return {
        insights: aiInsights
    };
};;
