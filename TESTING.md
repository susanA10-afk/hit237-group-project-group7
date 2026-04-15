# Testing Report
## HIT237 — Youth Justice & Crime App — Group 7
## Tester: Milan Sapkota
## Date: 16 April 2026

## Overview
I went through the app manually and tested all the main features to make sure everything works before we submit. Below are my results.

## Test Results

| Test | URL | Expected | Result |
|---|---|---|---|
| Login page loads | /login/ | Login form appears | Pass |
| Login works | /login/ | Goes to home after login | Pass |
| Wrong password rejected | /login/ | Shows error message | Pass |
| Home page loads | / | List of young persons shows | Pass |
| Search by first name | /?search=Sanish | Correct person shows | Pass |
| Search by last name | /?search=Chettri | Correct person shows | Pass |
| Risk colours show correctly | / | High is red, medium orange, low green | Pass |
| Pagination shows | / | Next and previous buttons appear | Pass |
| Add young person form loads | /youngperson/create/ | Form shows correctly | Pass |
| Add young person saves | /youngperson/create/ | Person appears in list after saving | Pass |
| View person details | /youngperson/1/ | Shows offences and interventions | Pass |
| Add offence form loads | /offence/create/ | Form with date picker shows | Pass |
| Add offence saves | /offence/create/ | Offence count updates in list | Pass |
| Add intervention | /intervention/create/ | Intervention saved correctly | Pass |
| Add court hearing | /courthearing/create/ | Hearing saved correctly | Pass |
| Dashboard loads | /dashboard/ | Only high risk persons show | Pass |
| Dashboard filters correctly | /dashboard/ | Medium and low risk not showing | Pass |
| Logout works | Click logout button | Redirects to login page | Pass |
| Pages require login | /youngperson/ | Redirects to login if not logged in | Pass |
| Add caseworker form loads | /caseworker/create/ | Form shows correctly | Pass |
| Add caseworker saves | /caseworker/create/ | Caseworker appears in intervention dropdown | Pass |
| Intervention list loads | /intervention/ | All interventions show with status colours | Pass |
| Add intervention with date picker | /intervention/create/ | Form saves correctly | Pass |

## What I noticed while testing

The search works well for both first and last name which is easy. The colour coding on risk levels makes it easy to quickly spot high risk cases. The dashboard only showing high risk persons is 
working as expected and I checked that medium and low risk people are not found there.

The date picker on the offence and hearing forms makes it much easier to enter dates compared to typing them manually. All forms validate correctly and show errors if required fields are missing.

## Summary

All 23 tests passed. The app is working correctly. No bugs or issues were found during testing.