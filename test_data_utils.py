"""
MAI201 Assignment 2 - pytest Unit Tests
Functions: load_csv | clean_phone | validate_email
"""
import os, re
import pandas as pd
import pytest


def load_csv(filepath: str) -> pd.DataFrame:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    df = pd.read_csv(filepath)
    if df.empty:
        raise ValueError(f"File is empty: {filepath}")
    return df

def clean_phone(phone) -> str:
    if phone is None:
        return ""
    digits = re.sub(r"\D", "", str(phone))
    if len(digits) != 10:
        return ""
    return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"

def validate_email(email) -> bool:
    if not email or not isinstance(email, str):
        return False
    pattern = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email.strip()))


class TestLoadCsv:

    def test_file_not_found_raises(self):
        with pytest.raises(FileNotFoundError, match="File not found"):
            load_csv("nonexistent_xyz.csv")

    def test_empty_file_raises(self, tmp_path):
        f = tmp_path / "empty.csv"
        f.write_text("customer_id,age,email\n")
        with pytest.raises(ValueError, match="File is empty"):
            load_csv(str(f))

    def test_successful_load_returns_dataframe(self, tmp_path):
        f = tmp_path / "good.csv"
        f.write_text("customer_id,age,email\nC001,30,test@example.com\n")
        result = load_csv(str(f))
        assert isinstance(result, pd.DataFrame) and len(result) == 1

    def test_correct_columns(self, tmp_path):
        f = tmp_path / "cols.csv"
        f.write_text("a,b,c\n1,2,3\n")
        assert list(load_csv(str(f)).columns) == ["a", "b", "c"]

    def test_all_rows_loaded(self, tmp_path):
        f = tmp_path / "rows.csv"
        f.write_text("id,val\n" + "\n".join(f"{i},{i*2}" for i in range(50)))
        assert len(load_csv(str(f))) == 50


class TestCleanPhone:

    def test_dashes(self):
        assert clean_phone("416-555-1234") == "416-555-1234"

    def test_dots(self):
        assert clean_phone("416.555.1234") == "416-555-1234"

    def test_parentheses(self):
        assert clean_phone("(416) 555-1234") == "416-555-1234"

    def test_plain_digits(self):
        assert clean_phone("4165551234") == "416-555-1234"

    def test_spaces(self):
        assert clean_phone("416 555 1234") == "416-555-1234"

    def test_too_few_digits(self):
        assert clean_phone("12345") == ""

    def test_too_many_digits(self):
        assert clean_phone("14165551234") == ""

    def test_letters_only(self):
        assert clean_phone("ABCDEFGHIJ") == ""

    def test_none_input(self):
        assert clean_phone(None) == ""

    def test_negative_number(self):
        assert clean_phone("-8437") == ""


class TestValidateEmail:

    def test_standard_email(self):
        assert validate_email("user@example.com") is True

    def test_subdomain(self):
        assert validate_email("user@mail.example.co.uk") is True

    def test_plus_tag(self):
        assert validate_email("user+tag@example.com") is True

    def test_numeric_local(self):
        assert validate_email("1234@example.com") is True

    def test_uppercase(self):
        assert validate_email("User.Name@Example.COM") is True

    def test_missing_at(self):
        assert validate_email("userexample.com") is False

    def test_missing_domain(self):
        assert validate_email("user@") is False

    def test_missing_tld(self):
        assert validate_email("user@domain") is False

    def test_at_only(self):
        assert validate_email("@domain.com") is False

    def test_double_at(self):
        assert validate_email("user@@domain.com") is False

    def test_empty_string(self):
        assert validate_email("") is False

    def test_none_input(self):
        assert validate_email(None) is False

    def test_whitespace_only(self):
        assert validate_email("   ") is False

    def test_surrounding_whitespace(self):
        assert validate_email("  user@example.com  ") is True
