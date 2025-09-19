export function validateEmail(value: string): boolean {
	const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
	return emailRegex.test(value);
}

export function validateName(value: string): boolean {
	return value.length > 2 && value.length < 20;
}

export function hasLength(value: string, length: number): boolean {
	return value.length >= length;
}

export function hasLetter(value: string): boolean {
	return /[a-zA-Z]/.test(value);
}

export function hasNumber(value: string): boolean {
	return /[0-9]/.test(value);
}
