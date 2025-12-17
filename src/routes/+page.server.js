export async function load({ fetch }) {
    try {
        const res = await fetch('https://api.rooted.hackclub.com/count');
        if (res.ok) {
            const data = await res.json();
            return { rsvpCount: data.count };
        }
    } catch (e) {
        console.log('Could not fetch count:', e);
    }
    return { rsvpCount: null };
}
