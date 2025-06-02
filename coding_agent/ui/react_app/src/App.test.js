import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';

test('renders learn react link', () => {
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});

test('can generate code', () => {
  render(<App />);
  const requirementsInput = screen.getByLabelText(/requirements/i);
  const generateButton = screen.getByText(/generate/i);

  fireEvent.change(requirementsInput, { target: { value: 'Create a simple web application' } });
  fireEvent.click(generateButton);

  // Check that the code is generated
  const codeElement = screen.getByText(/generated code/i);
  expect(codeElement).toBeInTheDocument();
});
