interface FieldProps {
    label: string;
    type: string;
    placeholder: string;
    value: string;
    onChange: (value: string) => void;
    autoComplete?: string;
    minLength?: number;
}

export default function Field({
    label,
    type,
    placeholder,
    value,
    onChange,
    autoComplete,
    minLength,
}: FieldProps) {
    return (
        <div className= "login-field" >
        <label>{ label } </label>

        < input
    required
    type = { type }
    placeholder = { placeholder }
    value = { value }
    autoComplete = { autoComplete }
    minLength = { minLength }
    onChange = {(event) => onChange(event.target.value)
}
      />
    </div>
  );
}