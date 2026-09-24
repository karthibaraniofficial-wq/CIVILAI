# CIVICFLOW AI — Known Issues & Mitigations

| Issue ID | Description | Impact | Mitigation Strategy | Status |
|---|---|---|---|---|
| KI-001 | Offline Hackathon Network Flakiness | Supabase Auth / Storage or Gemini API calls fail or latency spikes | Dual-persistence engine: Fallback to local SQLite and simulated Gemini structured agent engine when offline | MITIGATED |
| KI-002 | Ambiguous Citizen Grievance Input | Missing address, vague text description | Complaint Understanding Agent extracts nearest named landmarks; UI enforces map pin before submission | DESIGNED |
| KI-003 | Corrupt/Inappropriate Media Uploads | Spam images, blurry or non-civic photos | Vision Agent checks authenticity and calculates confidence; flags low-confidence images for human verification | DESIGNED |
